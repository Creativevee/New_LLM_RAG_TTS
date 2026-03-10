import torch
import soundfile as sf
from qwen_tts import Qwen3TTSModel

model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
    device_map="auto",
    dtype=torch.float32
)

wavs, sr = model.generate_custom_voice(
    text="Hello, this is a test audio from my project.",
    language="English",
    speaker="Ryan",
    instruct=""
)

sf.write("test_output.wav", wavs[0], sr)
print("done")