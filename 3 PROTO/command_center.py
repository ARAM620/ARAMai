import os
import json
import settings
from data_store import load_data
from tts import speak
from program_search import find_program_path

def execute_command(intent_or_text):
    internal_intents = ["notepad", "whale", "calculator", "settings", "json", "list"]
    
    if intent_or_text in internal_intents:
        intent = intent_or_text
    else:
        program_path = find_program_path(intent_or_text)
        if program_path:
            if settings.DEBUG:
                print(f"[DEBUG] '{intent_or_text}' 실행 경로 발견: {program_path}")
            os.startfile(program_path)
            return
        else:
            intent = intent_or_text

    if settings.DEBUG:
        print(f"[DEBUG] intent 기반 실행: {intent}")

    if intent == "notepad":
        print("메모장 실행")
        os.system("notepad.exe")
        
    elif intent == "whale":
        print("웨일 실행")
        whale_path = "C:\\Program Files\\Naver\\Naver Whale\\Application\\whale.exe"
        os.startfile(whale_path)
        
    elif intent == "calculator":
        print("계산기 실행")
        os.system("calc.exe")
        
    elif intent == "settings":
        print("설정 실행")
        os.system("control.exe")
        
    elif intent == "json":
        from data_store import load_data
        import json
        data = load_data()
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
    elif intent == "list":
        from data_store import load_data
        data = load_data()
        print("명령어 목록")
        for sentence, intent_name in data:
            print(f'"{sentence}" → {intent_name}')
            
    else:
        print("알 수 없는 명령입니다.")
