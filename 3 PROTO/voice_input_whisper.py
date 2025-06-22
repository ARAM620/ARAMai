import sounddevice as sd
import numpy as np
import whisper
import scipy.io.wavfile as wavfile
import tempfile

model = whisper.load_model("base")  # 또는 "tiny"

def listen_command_whisper():
    samplerate = 16000  # Whisper 권장 샘플링
    duration = 5  # 녹음 시간 (초)
    print("음성 명령 녹음 시작...")

    try:
        recording = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
        sd.wait()
    except Exception as e:
        print("녹음 실패:", e)
        return None

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wavfile.write(f.name, samplerate, recording)
        print("음성 인식 중...")
        try:
            result = model.transcribe(f.name, language="ko") or model.transcribe(f.name, language="en")
            print("인식 결과:", result["text"])
            return result["text"]
        except Exception as e:
            print("인식 실패:", e)
            return None
