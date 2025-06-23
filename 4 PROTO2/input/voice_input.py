import speech_recognition as sr
import numpy as np
import time

def listen_continuous(threshold=200, slience_limit=2):
    r = sr.Recognizer()
    mic = sr.Microphone()
    slience_count = 0

    with mic as source:
        r.adjust_for_ambient_noise(source)

        while True:
            print("음성 명령 대기 중...")
            audio = r.listen(source)

            raw_data = audio.get_raw_data()
            audio_np = np.frombuffer(raw_data, np.int16)
            volume = np.linalg.norm(audio_np)

            if volume < threshold:
                slience_count += 1
                if slience_count >= slience_limit:
                    break
                continue
            else:
                slience_count = 0

            try:
                text = r.recognize_google(audio, language="ko-KR")
                print(f"인식 결과: {text}")
                if text.strip().lower() in ["종료", "그만", "끝", "나가"]:
                    print("음성 인식 종료")
                    yield "__EXIT__"
                    break
                yield text
                time.sleep(0.3)

            except sr.UnknownValueError:
                print("인식 실패")
            except sr.RequestError:
                print("네트워크 오류 또는 API 문제 발생")
