#dict_generator.py

import json
import os

DICT_PATH = r"data\dictionary.json"

def load_dictionary():
    if not os.path.isfile(DICT_PATH):
        return {}
    with open(DICT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_dictionary(dic):
    with open(DICT_PATH, "w", encoding="utf-8") as f:
        json.dump(dic, f, ensure_ascii=False, indent=2)

def translate_korean_to_english(korean_name, dic):
    if korean_name in dic:
        return dic[korean_name]
    else:
        print(f"'{korean_name}'는 사전에 없습니다. 추가하시겠습니까? (y/n)")
        choice = input().strip().lower()
        if choice == 'y':
            print(f"'{korean_name}'의 영어 이름을 입력하세요")
            eng_name = input().strip()
            if eng_name:
                dic[korean_name] = eng_name
                save_dictionary(dic)
                print(f"사전에 '{korean_name}': '{eng_name}'가 추가되었습니다.")
                return eng_name
        print("단어가 추가되지 않았습니다.")
        return None
