#file_launcher.py

import os

def open_file(file_path: str) -> bool:
    try:
        if os.path.isfile(file_path):
            os.startfile(file_path)
            return True
        else:
            print(f"{file_path} 경로 탐색 실패")
            return False
    except Exception as e:
        print(f"파일 실행 실패: {e}")
        return False
    
