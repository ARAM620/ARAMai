#program_finder.py

import os
import sqlite3
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data"
DB_PATH = DATA_PATH / "programs.db"

START_MENU_PATHS = [
    Path(os.environ['ProgramData']) / "Microsoft" / "Windows" / "Start Menu" / "Programs",
    Path(os.environ['APPDATA']) / "Microsoft" / "Windows" / "Start Menu" / "Programs"
]

def initialize_db():
    DATA_PATH.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS programs (
            name TEXT PRIMARY KEY,
            path TEXT NOT NULL
        )
    ''')
    conn.commit()

    cur.execute('SELECT COUNT(*) FROM programs')
    if cur.fetchone()[0] == 0:
        all_programs = {}
        for base_path in START_MENU_PATHS:
            if not base_path.exists():
                continue
            for file in base_path.rglob("*"):
                if file.suffix.lower() in [".lnk", ".exe"]:
                    name = file.stem.lower()
                    all_programs[name] = str(file)

        for name, path in all_programs.items():
            cur.execute('INSERT INTO programs (name, path) VALUES (?, ?)', (name, path))
        conn.commit()

    conn.close()

def list_all_program_names() -> list[str]:
    initialize_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT name FROM programs ORDER BY name ASC')
    results = [row[0] for row in cur.fetchall()]
    conn.close()
    return results

def get_program_path(name: str) -> str | None:
    initialize_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT path FROM programs WHERE name = ?', (name.lower(),))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None
