from pathlib import Path
import torch
import soundfile as sf
from qwen_tts import Qwen3TTSModel

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs" / "audio"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
    device_map="auto",
    dtype=torch.float32
)

def text_to_speech(text):
    output_file = OUTPUT_DIR / "answer.wav"

    wavs, sr = model.generate_custom_voice(
        text=text,
        language="English",
        speaker="Ryan",
        instruct=""
    )

    sf.write(str(output_file), wavs[0], sr)
    return str(output_file)