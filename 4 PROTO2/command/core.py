from command.program_launcher import execute_program
from command.file_launcher import open_file
from command.directory_finder import find_and_open_directory

def handle_command(intent: str, target: str) -> bool:
    intent = intent.strip().lower()

    if intent == "1" or "앱 열기":
        return execute_program(target)

    elif intent == "2" or "파일 열기":
        return open_file(target)

    elif intent == "3" or "디렉토리 찾기":
        return find_and_open_directory(target)

    else:
        print(f"[알림] '{intent}'는 지원하지 않는 명령입니다.")
        return False
