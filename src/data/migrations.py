import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "app.db"

DDL = """
CREATE TABLE IF NOT EXISTS parametros (
id INTEGER PRIMARY KEY AUTOINCREMENT,
code TEXT UNIQUE NOT NULL,
nombre TEXT NOT NULL,
unidad TEXT
);
"""
def run_migrations(db_path: str | None = None):
    path = db_path or str(DB_PATH)
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.executescript(DDL)
    conn.commit()
    conn.close()
    print(f"Migración corriendo. DB en: {path}")

if __name__ == "__main__":
    run_migrations()

