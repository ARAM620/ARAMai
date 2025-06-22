from ai_core import load_model, predict_intent, retrain_model, add_training_example
from command_center import execute_command
from data_store import add_new_data, delete_data
from voice_input import listen_continuous
from wake_word import wait_for_wake_word
from program_search import find_program_path
import settings
import os

model, vectorizer = load_model()

def wake_and_listen_loop():
    while True:
        wait_for_wake_word("wakewords/아라암_ko_windows_v3_0_0.ppn")
        print("명령 대기중...")
        for command in listen_continuous():
            if not command:
                continue
            
            if command.lower() == "학습":
                sentence = input("학습할 문장\n:")
                intent = input("의도 입력\n:")
                add_training_example(sentence, intent)
                continue

            program_path = find_program_path(command)
            if program_path:
                print(f"프로그램 실행:{program_path}")
                os.startfile(program_path)
                continue
            
            intent = predict_intent(command, model, vectorizer)
            execute_command(intent)

if __name__ == "__main__":
    wake_and_listen_loop()

"""
print("시작")

while True:
    user_input = input("명령 입력\n: ")
    if user_input.lower() in ("exit", "종료"):
        print("종료")
        break
    elif user_input.lower() == "clear":
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
        continue    
    elif user_input.lower() == "debug on":
        settings.DEBUG = True
        print("디버그 모드 켜짐")
    elif user_input.lower() == "debug off":
        settings.DEBUG = False
        print("디버그 모드 꺼짐")
    elif user_input.lower() == "learn":
        sentence = input("문장 입력\n: ")
        intent = input("의도 입력\n: ")
        add_new_data(sentence, intent)
        retrain_model()
        model, vectorizer = load_model()
    elif user_input.lower() == "delete":
        sentence = input("삭제할 문장 입력\n: ")
        deleted = delete_data(sentence)
        if deleted:
            retrain_model()
            model, vectorizer = load_model()
    elif user_input.lower() == "voice":
        continuous_listen_mode()
    else:
        intent = predict_intent(user_input, model, vectorizer)
        execute_command(intent)
"""
