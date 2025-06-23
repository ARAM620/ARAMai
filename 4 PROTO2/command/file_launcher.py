#file_launcher.py

import os
from pathlib import Path

SEARCH_DIRS = [
    Path(os.environ["USERPROFILE"]) / "Documents",
    Path(os.environ["USERPROFILE"]) / "Downloads",
    Path(os.environ["USERPROFILE"]) / "Desktop"
]

def find_file_by_name(file_name: str) -> Path | None:
    file_name = file_name.lower()
    for search_dir in SEARCH_DIRS:
        for path in search_dir.rglob("*"):
            if path.is_file() and file_name in path.name.lower():
                return path
    return None

def open_file(file_name: str) -> bool:
    if os.path.isfile(file_name):
        os.startfile(file_name)
        return True
    
    path = find_file_by_name(file_name)
    if path:
        os.startfile(str(path))
        return True
    
    print(f"[파일 찾기 실패] '{file_name}' 파일을 찾을 수 없습니다.")
    return False
