import json
import os

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        print(f"{DATA_FILE} 파일이 존재하지 않습니다.")
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    data = load_data()
    if data:
        print("데이터 내용:")
        for sentence, intent in data:
            print(f"문장: {sentence} -> 의도: {intent}")
    else:
        print("불러온 데이터가 없습니다.")
