#program_launcher.py
import os
import subprocess
from utils.translator import translate_to_english
from utils.program_finder import get_program_path
from pathlib import Path

START_MENU_DIRS = [
    Path(os.environ["PROGRAMDATA"]) / "Microsoft" / "Windows" / "Start Menu" / "Programs",
    Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs"
]

BUILTIN_MAPPING = {
    "메모장": "notepad",
    "계산기": "calc",
    "그림판": "mspaint",
    "작업 관리자": "taskmgr",
    "명령 프롬프트": "cmd",
    "파일 탐색기": "explorer"
}

def execute_program_by_name(name: str) -> bool:
    
    name = name.strip().lower()
    
    if name in BUILTIN_MAPPING:
        try:
            subprocess.Popen(BUILTIN_MAPPING[name])
            print(f"{BUILTIN_MAPPING[name]} 실행 성공")
            return True
        except Exception as e:
            print(f"{name} 실행 실패")
            return False
        
    path = get_program_path(name)

    if not path:
        translated = translate_to_english(name)
        if translated != name:
            path = get_program_path(translated.lower())

    if path and os.path.exists(path):
        try:
            subprocess.Popen(['start', '', path], shell=True)
            print(f"{['start', '', path]} 실행 성공")
            return True
        except Exception as e:
            print(f"{name} 실행 실패: {e}")
            return False

    print(f"[실패] '{name}'에 해당하는 프로그램을 찾을 수 없습니다.")
    return False
