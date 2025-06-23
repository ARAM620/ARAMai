#main.py

from utils.intent_parser import parse_command
from command.core import handle_command
from utils.dict_generator import load_dictionary, save_dictionary, translate_korean_to_english
from input.voice_input import listen_continuous

def process_command(text, dic):
    parsed = parse_command(text)
    intent, target = parsed["intent"], parsed["target"]

    success = handle_command(intent, target)
    print(f"intent: {intent}, target: {target}")    
    if success:
        print(f"{target} 실행\n")
        return

    en_target = translate_korean_to_english(target, dic)
    if en_target is None:
        return

    print(f"intent: {intent}, target: {en_target}")
    success = handle_command(intent, en_target)
    print(f"{target} 실행\n" if success else f"{target} 실행 실패")    

def voice_mode(dic):
    print("음성 입력 모드")
    for text in listen_continuous():
        if text is None:
            continue

        if text == "__EXIT__":
            return "exit"

        if text.strip().lower() == "텍스트 입력" or "텍스트" in text.lower():
            print("텍스트 입력 모드로 전환")
            return "text"

        process_command(text, dic)

def text_mode(dic):
    print("텍스트 입력 모드")
    while True:
        text = input("input > ").strip()
        if not text:
            continue
        if "음성 입력" in text:
            print("음성 입력 모드로 전환")
            return "voice"
        if text in ["종료", "exit", "quit"]:
            return "exit"

        process_command(text, dic)

def main():
    print("ARAM AI 실행")
    dic = load_dictionary()
    mode = "voice"

    while True:
        if mode == "voice":
            mode = voice_mode(dic)
        elif mode == "text":
            mode = text_mode(dic)
        elif mode == "exit":
            print("ARAM AI 종료")
            break

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
