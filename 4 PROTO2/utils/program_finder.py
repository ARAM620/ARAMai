# program_finder.py

import os
import sqlite3
from pathlib import Path
import win32com.client

DATA_PATH = Path(__file__).resolve().parent.parent / "data"
DB_PATH = DATA_PATH / "programs.db"

START_MENU_PATHS = [
    Path(os.environ.get('ProgramData', '')) / "Microsoft" / "Windows" / "Start Menu" / "Programs",
    Path(os.environ.get('APPDATA', '')) / "Microsoft" / "Windows" / "Start Menu" / "Programs"
]

VALID_SUFFIXES = {".lnk", ".exe"}

def initialize_db():
    DATA_PATH.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS programs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            path TEXT NOT NULL,
            file_type TEXT NOT NULL,
            frequency INTEGER DEFAULT 0
        )
    ''')
    cur.execute("PRAGMA table_info(programs)")
    cols = [c[1] for c in cur.fetchall()]
    if 'frequency' not in cols:
        cur.execute('ALTER TABLE programs ADD COLUMN frequency INTEGER DEFAULT 0')
    cur.execute('SELECT COUNT(*) FROM programs')
    if cur.fetchone()[0] == 0:
        entries = find_all_programs()
        data = []
        for name, items in entries.items():
            for path, ftype in items:
                data.append((name, path, ftype))
        cur.executemany(
            'INSERT INTO programs (name, path, file_type) VALUES (?, ?, ?)',
            data
        )
    conn.commit()
    conn.close()

def resolve_lnk_path(lnk_path: Path) -> str:
    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(str(lnk_path))
        return shortcut.TargetPath
    except:
        return str(lnk_path)

def find_all_programs() -> dict[str, list[tuple[str, str]]]:
    result = {}
    for base in START_MENU_PATHS:
        if not base.exists():
            continue
        for file in base.rglob("*"):
            suf = file.suffix.lower()
            if suf not in VALID_SUFFIXES or not file.is_file():
                continue
            if suf == ".lnk":
                name = file.stem.lower()
                resolved = resolve_lnk_path(file)
                if not resolved or not Path(resolved).exists():
                    continue
                ftype = "lnk"
                path = resolved
            else:  # .exe
                name = file.stem.lower()
                path = str(file)
                ftype = "exe"
            result.setdefault(name, []).append((path, ftype))
    return result

def get_connection():
    initialize_db()
    return sqlite3.connect(DB_PATH)

def get_program_path(name: str) -> str | None:
    name = name.lower()
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute('SELECT id, path FROM programs WHERE name = ?', (name,))
        row = cur.fetchone()
        if row:
            cur.execute('UPDATE programs SET frequency = frequency+1 WHERE id=?', (row[0],))
            conn.commit()
            return row[1]
        like = f"%{name}%"
        cur.execute(
            'SELECT id, path FROM programs WHERE name LIKE ? ORDER BY frequency DESC',
            (like,)
        )
        row = cur.fetchone()
        if row:
            cur.execute('UPDATE programs SET frequency = frequency+1 WHERE id=?', (row[0],))
            conn.commit()
            return row[1]
    return None

def get_all_programs() -> list[tuple[str, str]]:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute('SELECT name, path FROM programs ORDER BY name ASC')
        return cur.fetchall()

def clean_invalid_entries():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute('SELECT id, path FROM programs')
        removed = False
        for _id, path in cur.fetchall():
            if not os.path.exists(path):
                cur.execute('DELETE FROM programs WHERE id=?', (_id,))
                removed = True
        if removed:
            conn.commit()
