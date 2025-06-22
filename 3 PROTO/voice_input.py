import speech_recognition as sr
import numpy as np
import time

def listen_continuous(threshold=300, slience_limit=3):
    r = sr.Recognizer()
    mic = sr.Microphone()
    slience_count = 0

    with mic as source:
        r.adjust_for_ambient_noise(source)
        print("계속 듣기 모드 시작")

        while True:
            print("음성 명령 대기 중...")
            audio = r.listen(source)

            raw_data = audio.get_raw_data()
            audio_np = np.frombuffer(raw_data, np.int16)
            volume  = np.linalg.norm(audio_np)

            if volume < threshold:
                slience_count += 1
                if slience_count >= slience_limit:
                    print("감지 종료")
                    break
                continue
            else:
                slience_count = 0

            try:
                text = r.recognize_google(audio, language="ko-KR")
                print(f"음성 인식 결과: {text}")
                if text.strip() in ["종료", "그만", "끝", "나가"]:
                    print("음성 인식 모드 종료")
                    break
                yield text
                time.sleep(0.5)
            except sr.UnknownValueError:
                print("인식 실패")
            except sr.RequestError:
                print("음성 인식 서비스 오류")
