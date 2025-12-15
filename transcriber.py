from faster_whisper import WhisperModel

print("Transcriber started")

input_file_path= "data/file.mp3"
output_file_path= "data/file.txt"

model = WhisperModel(model_size_or_path="./model/", device="cuda")

segments, _ = model.transcribe(input_file_path, "ru")
with open(output_file_path, "w", encoding="utf-8") as file:
    for segment in segments:
        file.write(segment.text)

print("Transcriber stopped")