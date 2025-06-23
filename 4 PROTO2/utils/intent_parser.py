#intent_parser.py

import re

def parse_command(text: str) -> dict:
    text = text.strip().lower()
    intent = None

    if "파일" in text and "열" in text:
        match = re.search(r"(.*?)(파일.*?)열", text)
        if match:
            target = match.group(1).strip()
        else:
            target = text.replace("파일", "").replace("열어줘", "").strip()
        return {"intent": "파일 열기", "target": target}

    if any(word in text for word in ["폴더", "디렉터리", "찾", "열", "보여"]):
        if "파일" not in text and "앱" not in text:
            match = re.search(r"(.*?)(폴더|디렉터리|찾|열|보여)", text)
            if match:
                target = match.group(1).strip()
                return {"intent": "디렉터리 찾기", "target": target}
            
    if any(word in text for word in ["켜", "실행", "열어", "시작"]):
        match = re.search(r"(.*?)(앱|프로그램|열어|켜|실행)", text)
        if match:
            target = match.group(1).strip()
            return {"intent": "앱 열기", "target": target}

    if intent is None:
        intent = "앱 열기"

    return {"intent": intent, "target": text}
