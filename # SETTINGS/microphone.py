import whisper

model = whisper.load_model("base")  # tiny/base/small/medium/large
result = model.transcribe("audio.wav")
print(result["text"])
