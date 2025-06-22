import pvporcupine
import pyaudio
import struct

def wait_for_wake_word(ppn_path):
    access_key = "e62TzbmB6EwHOoX5Guawix1xZGtyhSBWS516fUgioWvQMIKICmLO8g=="

    porcupine = pvporcupine.create(
        access_key=access_key,
        keyword_paths=["C:\\Users\\SungEun\\Desktop\\ARAM\\3 PROTO\\wakewords\\아라암_ko_windows_v3_0_0.ppn"],
        model_path=r"C:\Users\SungEun\Desktop\ARAM\3 PROTO\wakewords\porcupine_params_ko.pv"
    )

    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("대기 중...")

    try:
        while True:
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            result = porcupine.process(pcm)
            if result >= 0:
                print("아람 감지됨")
                break
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()
        porcupine.delete()
