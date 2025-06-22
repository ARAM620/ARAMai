import pickle
import os
import json
from train_model import train_model

def load_model():
    with open("intent_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)
    return model, vectorizer

model, vectorizer= load_model()

def predict_intent(text):
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        for sentence, intent in data:
            if sentence.strip() == text.strip():
                return intent
    except FileNotFoundError:
        pass

    X_test = vectorizer.transform([text])
    pred = model.predict(X_test)
    return pred[0]

def execute_command(command):
    intent = predict_intent(command)

    if intent == "notepad":
        print("메모장을 실행합니다.")
        os.system("notepad.exe")

    elif intent == "whale":
        print("웨일을 실행합니다.")
        whale_path = "C:\\Program Files\\Naver\\Naver Whale\\Application\\whale.exe"
        os.startfile(whale_path)

    elif intent == "calculator":
        print("계산기를 실행합니다.")
        os.system("calc.exe")

    elif intent == "settings":
        print("설정을 실행합니다.")
        os.system("control.exe")

    elif intent == "json":
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        print(data)

    else:
        print("알 수 없는 명령입니다.")

def  add_new_command():
    sentence = input("학습할 문장을 입력하세요.\n:")
    intent = input("의 문장의 의도는 무엇인가요?\n:")

    try:
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append([sentence, intent])

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("[+] 새로운 데이터가 추가되었습니다. 모델을 재학습합니다...")
    train_model()
    global model, vectorizer
    model, vectorizer = load_model()

if __name__ == "__main__":
    while True:
        user_input = input("명령어 입력\n:")
        if user_input.lower() == "exit" or user_input.lower() == "종료":
            print("프로그램을 종료합니다.")
            break
        elif user_input.lower() == "learn":
            add_new_command()
        else:
            execute_command(user_input)
