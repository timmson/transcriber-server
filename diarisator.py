import torch
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook

print("Starting")

input_file_path= "data/file.mp3"
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-community-1",
    token="HUGGINGFACE_ACCESS_TOKEN")

pipeline.to(torch.device("cuda"))

with ProgressHook() as hook:
    output = pipeline(input_file_path, hook=hook)  # runs locally

for turn, speaker in output.speaker_diarization:
    print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")