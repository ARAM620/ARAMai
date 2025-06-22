import os

command_keyword = {
    "메모장": ["메모장", "notepad", "메모", "memo"],
    "웨일": ["웨일", "whale", "internet", "whlae"]
    }

def excute_command(command):
    command = command.lower()

    for keyword in command_keyword["웨일"]:
        print("웨일을 실행합니다/")
        whale_path = "C:\\Program Files\\Naver\\Naver Whale\\Application\\whale.exe"
        os.startfile(whale_path)
        return

    for keyword in command_keyword["메모장"]:
        print("메모장을 실행합니다.")
        os.system("notepad.exe")
        return


    print("알 수 없는 명령입니다.")

if __name__ == "__main__":
    while True:
        user_input = input("무엇을 도와드릴까요?\n")
        if user_input.lower() == "exit" or user_input.lower() == "종료":
            print("프로그램을 종료합니다.")
            break
        excute_command(user_input)
