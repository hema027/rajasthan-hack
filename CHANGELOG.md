# Changelog

All notable changes to the CloneTrace project will be documented in this file.

## [v2.0.0] - 2026-10-07

### Added
- Added `prototype_scorer` section to `config.yaml` for rule-based heuristics scoring.
- Schema migration to version 2.0.0 (`contract/schema.sql`, `db.py`).
- Added `requests` (JSON list of attempted requests) and `dead_reason` columns to `fetches` table.
- Added `corpus_meta` table for synthetic corpus ground truth tracking (kit_id, campaign_id, template, brand, cloaked, perturbation_level, exfil_type, display_domain).
- Added `fetch` and `corpus` configuration sections to `config.yaml`.
- Added `scripts/run.ps1` cross-platform PowerShell runner.
- Added `corpus/` package owned by Data Agent.

## [v0-skeleton] - 2026-10-07

### Added
- Repository initialization and core walking skeleton.
- Database schema (`contract/schema.sql`) for observations, fetches, features, verdicts, indicators, campaigns, campaign_members, and labels.
- Contract data models in `contract/models.py` with Pydantic v2.
- Ingestion engine in `detect/ingest.py` supporting URL, UPI VPA (excluding email formats), and Indian phone number extraction.
- Deterministic stubs in `detect/` (`fetcher.py`, `features.py`, `model.py`, `apk.py`, `eval.py`) with `# TODO(step N)` markers.
- Graph construction engine in `graph/build.py` implementing IDF indicator weighting, hub filtering on weak types, and pyvis bipartite network construction.
- Two-stage campaign clustering engine in `graph/cluster.py` with strong edge connected components and split-only Louvain modularity optimization.
- Deterministic synthetic generator in `scripts/make_seed.py` and `graph/synth.py` with 41 seed observations across 5 campaigns and 10 benign records.
- Automated takedown pack PDF generation with ReportLab in `report/takedown.py`.
- Interactive Streamlit dashboard in `app/streamlit_app.py` with Threat Feed, Campaign Clusters, and Takedown Reports.
- Automated end-to-end pipeline runner in `pipeline.py`.
- Unit and smoke test suites in `tests/` with isolated temporary SQLite database fixture.
- Project automation in `Makefile`.
