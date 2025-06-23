#directory_finder.py

import os
from pathlib import Path

COMMON_DIRECTORIES = {
    "다운로드": Path(os.environ["USERPROFILE"]) / "Downloads",
    "문서": Path(os.environ["USERPROFILE"]) / "Documents",
    "바탕화면": Path(os.environ["USERPROFILE"]) / "Desktop",
    "사진": Path(os.environ["USERPROFILE"]) / "Pictures",
    "음악": Path(os.environ["USERPROFILE"]) / "Music",
    "비디오": Path(os.environ["USERPROFILE"]) / "Videos",
}

SEARCH_ROOTS = list(COMMON_DIRECTORIES.values()) + [Path(os.environ["USERPROFILE"])]

def find_directory_by_name(name: str) -> Path | None:
    name = name.lower()
    for root in SEARCH_ROOTS:
        for path in root.rglob("*"):
            if path.is_dir() and name in path.name.lower():
                return path
    return None

def find_and_open_directory(name: str) -> bool:
    if name in COMMON_DIRECTORIES:
        path = COMMON_DIRECTORIES[name]
        os.startfile(str(path))
        return True

    path = find_directory_by_name(name)
    if path:
        os.startfile(str(path))
        return True

    print(f"[폴더 찾기 실패] '{name}' 폴더를 찾을 수 없습니다.")
    return False
