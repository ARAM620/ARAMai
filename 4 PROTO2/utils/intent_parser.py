#intent_parser.py

import re

def parse_command(text: str) -> dict:
    text = text.strip().lower()
    intent = None
    target = text

    # 1. 시스템 명령 우선 처리
    if any(word in text for word in ["시스템 종료", "재시작", "절전", "대기"]):
        intent = "시스템 명령"
        return {"intent": intent, "target": target}

    # 2. 파일 열기 의도 판단
    if "파일" in text and "열" in text:
        match = re.search(r"(.*?)(파일.*?)열", text)
        if match:
            target = match.group(1).strip()
        else:
            # fallback: '파일', '열어줘' 제거 후 트림
            target = text.replace("파일", "").replace("열어줘", "").strip()
        intent = "파일 열기"
        return {"intent": intent, "target": target}

    # 3. 디렉터리 찾기 의도 판단
    if any(word in text for word in ["폴더", "디렉터리", "찾", "열", "보여"]) and "파일" not in text and "앱" not in text:
        match = re.search(r"(.*?)(폴더|디렉터리|찾|열|보여)", text)
        if match:
            target = match.group(1).strip()
        intent = "디렉터리 찾기"
        return {"intent": intent, "target": target}

    # 4. 앱 열기 의도 판단
    if any(word in text for word in ["켜", "실행", "열어", "시작"]):
        match = re.search(r"(.*?)(앱|프로그램|열어|켜|실행)", text)
        if match:
            target = match.group(1).strip()
        intent = "앱 열기"
        return {"intent": intent, "target": target}

    # 5. 기본 fallback (앱 열기)
    intent = "앱 열기"
    return {"intent": intent, "target": target}
