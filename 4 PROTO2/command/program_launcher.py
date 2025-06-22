#program_launcher.py
import os
import subprocess
import win32com.client
import shutil
from utils.translator import translate_to_english
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

def find_shortcut_by_name(name: str):
    for directory in START_MENU_DIRS:
        for shortcut in directory.rglob("*.lnk"):
            if name.lower() in shortcut.stem.lower():
                return shortcut
    return None


def search_start_menu_shortcuts(name: str):
    start_menu_paths = [
        os.environ["APPDATA"] + "\\Microsoft\\Windows\\Start Menu\\Programs",
        os.environ["PROGRAMDATA"] + "\\Microsoft\\Windows\\Start Menu\\Programs",
    ]
    lnk_files = []
    for path in start_menu_paths:
        for root, _, files in os.walk(path):
            for file in files:
                if file.lower().endswith(".lnk") and name.lower() in file.lower():
                    lnk_files.append(os.path.join(root, file))
    return lnk_files

def resolve_shortcut_target(shortcut_path: Path) -> str:
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(str(shortcut_path))
    return shortcut.TargetPath

def search_exe_in_program_files(name: str):
    search_dirs = [
        os.environ.get("ProgramFiles", ""),
        os.environ.get("ProgramFiles(x86)", ""),
        os.environ.get("LOCALAPPDATA", ""),
    ]
    for base_dir in search_dirs:
        for root, _, files in os.walk(base_dir):
            for file in files:
                if file.lower().endswith(".exe") and name.lower() in file.lower():
                    return os.path.join(root, file)
    return None

def execute_program_by_name(name: str):
    if name in BUILTIN_MAPPING:
        os.system(BUILTIN_MAPPING[name])
        return True

    shortcut = find_shortcut_by_name(name)
    if shortcut:
        target_path = resolve_shortcut_target(shortcut)
        subprocess.Popen([target_path])
        return True

    translated_name = translate_to_english(name)
    if translated_name and translated_name != name:
        shortcut = find_shortcut_by_name(translated_name)
        if shortcut:
            target_path = resolve_shortcut_target(shortcut)
            subprocess.Popen([target_path])
            return True

    print(f"[실패] '{name}'에 해당하는 프로그램을 찾을 수 없습니다.")
    return False
