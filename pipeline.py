import argparse
import json
import logging
from pathlib import Path
from db import get_conn, init_db
from detect.features import extract_features
from detect.model import score
from detect.fetcher import fetch
from graph.enrich import enrich
from graph.build import build_graph
from graph.cluster import cluster
from scripts.make_seed import make_seed

logger = logging.getLogger("clonetrace.pipeline")


def run_pipeline(mode: str = "seed") -> list:
    """
    Executes the end-to-end CloneTrace analysis and clustering pipeline.
    Modes:
      - 'seed': runs on deterministic seed dataset (default)
      - 'corpus': runs on synthetic corpus observations with prototype scoring
    Idempotent.
    """
    # 1. Initialize DB
    init_db()

    conn = get_conn()

    if mode == "corpus":
        try:
            # Check for corpus observations
            cur = conn.execute("""
                SELECT o.id FROM observations o
                JOIN corpus_meta cm ON o.id = cm.obs_id
                ORDER BY o.id ASC
            """)
            corpus_obs_ids = [r["id"] for r in cur.fetchall()]

            if not corpus_obs_ids:
                logger.info("No corpus observations found; building synthetic corpus...")
                from corpus.build_corpus import build_corpus
                build_corpus()
                cur = conn.execute("""
                    SELECT o.id FROM observations o
                    JOIN corpus_meta cm ON o.id = cm.obs_id
                    ORDER BY o.id ASC
                """)
                corpus_obs_ids = [r["id"] for r in cur.fetchall()]

            target_obs_ids = corpus_obs_ids
        finally:
            conn.close()

        logger.info("Processing %d corpus observations...", len(target_obs_ids))

        # Ensure fetched, extracted, scored, and enriched
        for o_id in target_obs_ids:
            # Check if fetched
            c = get_conn()
            try:
                fetches_cnt = c.execute("SELECT COUNT(*) as cnt FROM fetches WHERE obs_id = ?", (o_id,)).fetchone()["cnt"]
            finally:
                c.close()
            if fetches_cnt < 2:
                fetch(o_id)

            extract_features(o_id)
            score(o_id, force=True)
            enrich(o_id)

        # Build graph and cluster corpus observations separately
        G = build_graph(obs_ids=target_obs_ids)
        campaigns = cluster(G, obs_ids=target_obs_ids)

        c = get_conn()
        try:
            placeholders = ",".join("?" for _ in target_obs_ids)
            cur = c.execute(
                f"SELECT COUNT(*) as flagged FROM verdicts WHERE obs_id IN ({placeholders}) AND label IN ('phish', 'suspicious')",
                target_obs_ids
            )
            flagged_obs = cur.fetchone()["flagged"]
        finally:
            c.close()

        total_obs = len(target_obs_ids)

    else:
        # Seed mode
        try:
            cur = conn.execute("SELECT COUNT(*) as cnt FROM observations")
            obs_count = cur.fetchone()["cnt"]

            if obs_count == 0:
                seed_path = Path("data/seed.json")
                if not seed_path.exists():
                    make_seed(seed_path)
                with open(seed_path, "r", encoding="utf-8") as f:
                    seed_data = json.load(f)

                with conn:
                    for item in seed_data:
                        obs_id = item["id"]
                        conn.execute(
                            """
                            INSERT INTO observations (id, url, source, source_ref, raw_text, first_seen, is_synthetic)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            """,
                            (
                                obs_id,
                                item.get("url"),
                                item.get("source"),
                                item.get("source_ref"),
                                item.get("raw_text"),
                                item.get("first_seen"),
                                item.get("is_synthetic", 1)
                            )
                        )

                        # Indicators
                        for ind in item.get("indicators", []):
                            conn.execute(
                                "INSERT OR IGNORE INTO indicators (obs_id, type, value) VALUES (?, ?, ?)",
                                (obs_id, ind["type"], ind["value"])
                            )

                        # Verdicts
                        verd = item.get("verdict", {})
                        if verd:
                            conn.execute(
                                """
                                INSERT OR REPLACE INTO verdicts (obs_id, score, label, brand, signals, model_version)
                                VALUES (?, ?, ?, ?, ?, ?)
                                """,
                                (
                                    obs_id,
                                    verd.get("score", 0.0),
                                    verd.get("label", "unknown"),
                                    verd.get("brand"),
                                    json.dumps(verd.get("signals", {})),
                                    verd.get("model_version", "v0-seed")
                                )
                            )

                        # Labels
                        lbl = item.get("labels", {})
                        if lbl:
                            conn.execute(
                                """
                                INSERT OR REPLACE INTO labels (obs_id, label, split, heldout_brand, campaign_gt)
                                VALUES (?, ?, ?, ?, ?)
                                """,
                                (
                                    obs_id,
                                    lbl.get("label"),
                                    lbl.get("split", "train"),
                                    lbl.get("heldout_brand", 0),
                                    lbl.get("campaign_gt", 0)
                                )
                            )

            cur = conn.execute("SELECT id FROM observations WHERE id < 1000")
            seed_ids = [r["id"] for r in cur.fetchall()]
            if not seed_ids:
                cur = conn.execute("SELECT id FROM observations")
                seed_ids = [r["id"] for r in cur.fetchall()]
        finally:
            conn.close()

        for o_id in seed_ids:
            extract_features(o_id)
            score(o_id)
            enrich(o_id)

        G = build_graph(obs_ids=seed_ids)
        campaigns = cluster(G, obs_ids=seed_ids)

        c = get_conn()
        try:
            placeholders = ",".join("?" for _ in seed_ids)
            cur = c.execute(
                f"SELECT COUNT(*) as flagged FROM verdicts WHERE obs_id IN ({placeholders}) AND label IN ('phish', 'suspicious')",
                seed_ids
            )
            flagged_obs = cur.fetchone()["flagged"]
        finally:
            c.close()

        total_obs = len(seed_ids)

    print("========================================")
    print(f"  CloneTrace Pipeline Summary ({mode.upper()})  ")
    print("========================================")
    print(f"Total Observations       : {total_obs}")
    print(f"Flagged Phish/Suspicious : {flagged_obs}")
    print(f"Campaigns Discovered     : {len(campaigns)}")
    print("----------------------------------------")
    for camp in campaigns:
        brands_str = ", ".join(camp.brands) if camp.brands else "N/A"
        print(f"  * {camp.name:<12} | Size: {camp.size:<2} | Brands: {brands_str}")
    print("========================================")

    return campaigns


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CloneTrace Pipeline Runner")
    parser.add_argument("--corpus", action="store_true", help="Run pipeline on synthetic corpus observations")
    args = parser.parse_args()

    if args.corpus:
        run_pipeline(mode="corpus")
    else:
        run_pipeline(mode="seed")
