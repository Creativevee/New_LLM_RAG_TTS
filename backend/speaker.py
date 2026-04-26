import uuid

from gtts import gTTS

from config import AUDIO_DIR


def synthesize(text: str) -> str:
    if not text.strip():
        return ""
    name = f"reply_{uuid.uuid4().hex[:10]}.mp3"
    path = AUDIO_DIR / name
    gTTS(text=text, lang="en", slow=False).save(str(path))
    return name
