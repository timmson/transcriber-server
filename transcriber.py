from faster_whisper import WhisperModel

print("Transcriber started")

input_file_path= "data/0006e35833b14712_2025-12-18_14-00-05.mp4"
output_file_path= "data/0006e35833b14712_2025-12-18_14-00-05.txt"

model = WhisperModel(model_size_or_path="./model/", device="cuda")

segments, _ = model.transcribe(input_file_path, "ru")
with open(output_file_path, "w", encoding="utf-8") as file:
    for segment in segments:
        file.write(segment.text)

print("Transcriber stopped")