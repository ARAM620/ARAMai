#main.py

from utils.intent_parser import parse_command
from command.core import handle_command
from utils.dict_generator import load_dictionary, save_dictionary, translate_korean_to_english

def main():
    print("앱, 파일, 디렉터리 실행 명령 입력")

    dic = load_dictionary()

    while True:
        text = input("input > ").strip()
        if text.lower() in ["종료", "exit", "quit"]:
            break

        parsed = parse_command(text)
        intent, target = parsed["intent"], parsed["target"]

        en_target = translate_korean_to_english(target, dic)
        if en_target is None:
            continue

        print(f"intent: {intent}, target: {en_target}")
        success = handle_command(intent, en_target)
        print(f"{target} 실행\n" if success else f"{target} 실행 실패")

'''
INTENT_MAP = {
    "1": "앱 열기",
    "2": "파일 열기",
    "3": "디렉터리 찾기"
}

def main():
    print("지원하는 intent: [1] 앱 열기, [2] 파일 열기, [3] 디렉터리 찾기")

    while True:
        intent = input("Intent > ").strip()
        if intent.lower() in ["종료", "exit", "quit"]:
            print("종료합니다.")
            break

        intent = INTENT_MAP.get(intent, intent)

        target = input("Target > ").strip()
        if not target:
            print("대상을 입력하지 않았습니다.\n")
            continue

        success = handle_command(intent, target)
        if not success:
            print("명령 실행 실패.\n")
'''
if __name__ == "__main__":
    main()
