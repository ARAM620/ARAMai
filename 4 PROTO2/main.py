#main.py
import re
import threading
import time

from utils.intent_parser import parse_command
from command.core import handle_command
from utils.dict_generator import load_dictionary, save_dictionary, translate_korean_to_english
from input.voice_input import listen_continuous

def parse_schedule(text):
    match = re.search(r"(\d+)\s*(초|분|시간)\s*후", text)
    if not match:
        return None
    amount = int(match.group(1))
    unit = match.group(2)

    if unit == "초":
        return amount
    elif unit == "분":
        return amount * 60
    elif unit == "시간":
        return amount * 3600
    return None

def run_scheduled_command(delay, command_text, dictionary):
    def task():
        time.sleep(delay)
        print(f"[예약 실행] {command_text}")
        process_command(command_text, dictionary)
    threading.Thread(target=task, daemon=True).start()

def process_command(text, dic):
    delay = parse_schedule(text)
    if delay is not None:
        cleaned_text = re.sub(r"\d+\s*(초|분|시간)\s*후", "", text).strip()
        if not cleaned_text:
            print("[오류] 실행할 명령이 없습니다. 예약 등록 취소됨.\n")
            return        
        print(f"[예약 등록] {delay}초 후 실행 예약: {cleaned_text}")
        run_scheduled_command(delay, cleaned_text, dic)
        return
    
    parsed = parse_command(text)
    intent, target = parsed["intent"], parsed["target"]

    success = handle_command(intent, target)
    print(f"intent: {intent}, target: {target}")    
    if success:
        print(f"{target} 실행\n")
        return
    print(f"[정보] '{target}' 직접 실행 실패, 번역을 시도합니다...")

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
