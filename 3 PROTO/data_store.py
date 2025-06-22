import json
import os

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_new_data(sentence, intent):
    data = load_data()
    data.append([sentence, intent])
    save_data(data)
    print("저장 완료")

def delete_data(sentence):
    data = load_data()
    new_data = [item for item in data if item[0].strip().lower() != sentence.strip().lower()]
    if len(new_data) == len(data):
        print("삭제할 명령어가 없습니다.")
        return False
    save_data(new_data)
    print(f'"{sentence}" 명령어가 삭제되었습니다.')
    return True
