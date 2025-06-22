#directory_finder.py

import os

COMMON_DIRECTORIES = {
    "다운로드": os.path.join(os.environ["USERPROFILE"], "Downloads"),
    "문서": os.path.join(os.environ["USERPROFILE"], "Documents"),
    "바탕화면": os.path.join(os.environ["USERPROFILE"], "Desktop"),
    "사진": os.path.join(os.environ["USERPROFILE"], "Pictures"),
    "음악": os.path.join(os.environ["USERPROFILE"], "Music"),
    "비디오": os.path.join(os.environ["USERPROFILE"], "Videos"),
}

def find_and_open_directory(name: str) -> bool:
    name = name.strip().lower()

    if name in COMMON_DIRECTORIES:
        path = COMMON_DIRECTORIES[name]
    else:
        path = name

    try:
        if os.path.isdir(path):
            os.startfile(path)
            return True
        else:
            print(f"{path} 경로 탐색 실패")
            return False
    except Exception as e:
        print(f"폴더 탐색 실패: {e}")
        return False
