import os
import sqlite3
from pathlib import Path
import pythoncom
import win32com.client
import subprocess

DB_PATH = Path(r"C:\Users\SungEun\Desktop\ARAM\4 PROTO2\data") / "program_cache.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

COMMON_PROGRAM_FOLDERS = [
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    "C:\\Users\\%USERNAME%\\AppData\\Local\\Programs",
    "C:\\Users\\%USERNAME%\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs",
    "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs",
]

BUILTIN_MAPPING = {
    "메모장": "notepad",
    "계산기": "calc",
    "그림판": "mspaint",
    "작업 관리자": "taskmgr",
    "명령 프롬프트": "cmd",
    "파일 탐색기": "explorer"
}

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS program_cache (
            name TEXT PRIMARY KEY,
            path TEXT NOT NULL,
            file_type TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_to_cache(name: str, path: str, file_type: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('REPLACE INTO program_cache (name, path, file_type) VALUES (?, ?, ?)',
                (name.lower(), path, file_type))
    conn.commit()
    conn.close()

def load_from_cache(name: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT path, file_type FROM program_cache WHERE name = ?', (name.lower(),))
    row = cur.fetchone()
    conn.close()
    if row and os.path.exists(row[0]):
        return row[0], row[1]
    return None

def resolve_lnk(lnk_path: Path) -> str | None:
    try:
        pythoncom.CoInitialize()
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(str(lnk_path))
        target = shortcut.TargetPath
        return target if target and Path(target).exists() else None
    except:
        return None

def find_program_path(name: str) -> tuple[str, str] | None:
    init_db()

    cached = load_from_cache(name)
    if cached:
        return cached

    name = name.lower()
    for folder in COMMON_PROGRAM_FOLDERS:
        folder = os.path.expandvars(folder)
        if not os.path.exists(folder):
            continue
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_lower = file.lower()
                if file_lower.startswith(name):
                    full_path = os.path.join(root, file)
                    if file_lower.endswith(".exe"):
                        save_to_cache(name, full_path, "exe")
                        return full_path, "exe"
                    elif file_lower.endswith(".lnk"):
                        target = resolve_lnk(Path(full_path))
                        if target:
                            save_to_cache(name, full_path, "lnk")
                            return full_path, "lnk"
    return None

def execute_program(name: str) -> bool:
    name = name.strip().lower()
    if name in BUILTIN_MAPPING:
        try:
            subprocess.Popen(BUILTIN_MAPPING[name])
            print(f"[내장 실행 성공] {BUILTIN_MAPPING[name]}")
            return True
        except Exception as e:
            print(f"[내장 실행 실패] {name}: {e}")
            return False

    found = find_program_path(name)
    if not found:
        print(f"[실패] '{name}'에 해당하는 실행 파일이나 바로가기를 찾을 수 없습니다.")
        return False

    path, ftype = found
    try:
        if ftype == "lnk":
            os.startfile(path)
        else:
            subprocess.Popen(path)
        print(f"[실행 성공] {path}")
        return True
    except Exception as e:
        print(f"[실행 실패] {path}: {e}")
        return False

if __name__ == "__main__":
    init_db()
    target_name = input("실행할 프로그램 이름 입력: ")
    execute_program(target_name)
