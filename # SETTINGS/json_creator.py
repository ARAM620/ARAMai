import json
import os

DATA_FILE = "data.json"

def create_initial_data():
    if not os.path.exists(DATA_FILE):
        initial_data = [
            ["메모장 열어줘", "notepad"],
            ["계산기 열어줘", "calculator"],
            ["웨일 켜", "whale"],
            ["설정 열어줘", "settings"],
            ["학습 데이터 보여줘", "json"],
            ["명령어 목록 보여줘", "list"]
        ]
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(initial_data, f, ensure_ascii=False, indent=2)
        print(f"{DATA_FILE} 파일 생성 완료")
    else:
        print(f"{DATA_FILE} 파일이 이미 존재함")

if __name__ == "__main__":
    create_initial_data()
