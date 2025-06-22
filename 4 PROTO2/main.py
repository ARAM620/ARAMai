#main.py
from command.core import handle_command

def main():
    while True:
        command_text = input("실행할 프로그램 이름\n:").strip()
        if command_text.lower() in ("exit", "종료"):
            print("ARAM 종료")
            break
        handle_command(command_text)

if __name__ == "__main__":
    main()
