import os
import sqlite3
from pathlib import Path
from typing import Optional

SCHEMA_VERSION = "2.0.0"

def get_db_path() -> Path:
    return Path(os.environ.get("CLONETRACE_DB", "data/db/clonetrace.db"))

def get_conn(db_path: Optional[Path] = None) -> sqlite3.Connection:
    target_path = db_path if db_path is not None else get_db_path()
    target_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(target_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db(db_path: Optional[Path] = None) -> None:
    target_path = db_path if db_path is not None else get_db_path()
    schema_path = Path(__file__).parent / "contract" / "schema.sql"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    with get_conn(target_path) as conn:
        conn.executescript(schema_sql)
        # Ensure migrations for version 2.0.0 columns if table pre-existed
        cur = conn.execute("PRAGMA table_info(fetches)")
        cols = {r["name"] for r in cur.fetchall()}
        if cols:
            if "requests" not in cols:
                conn.execute("ALTER TABLE fetches ADD COLUMN requests TEXT")
            if "dead_reason" not in cols:
                conn.execute("ALTER TABLE fetches ADD COLUMN dead_reason TEXT")
        conn.commit()
