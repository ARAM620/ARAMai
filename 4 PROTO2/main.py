from command.core import handle_command

def main():
    print("지원하는 intent: [1] 앱 열기, [2] 파일 열기, [3] 디렉토리 찾기")

    while True:
        intent = input("Intent > ").strip()
        if intent.lower() in ["종료", "exit", "quit"]:
            print("종료합니다.")
            break

        target = input("Target > ").strip()
        if not target:
            print("대상을 입력하지 않았습니다.\n")
            continue

        success = handle_command(intent, target)
        if not success:
            print("명령 실행 실패.\n")

if __name__ == "__main__":
    main()
