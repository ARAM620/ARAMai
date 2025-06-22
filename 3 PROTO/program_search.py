import os

COMMON_PROGRAM_FOLDERS = [
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    "C:\\Users\\%USERNAME%\\AppData\\Local\\Programs",
]

def find_program_path(name):
    for folder in COMMON_PROGRAM_FOLDERS:
        if '%' in folder:
            folder = os.path.expandvars(folder)
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.lower().startswith(name.lower()) and file.endswith(".exe"):
                    return os.path.join(root, file)
    return None
