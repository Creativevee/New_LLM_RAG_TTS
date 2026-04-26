import logging
import platform
import shutil
import subprocess
import uuid

from config import AUDIO_DIR

logger = logging.getLogger(__name__)


def synthesize(text: str) -> str:
    if not text.strip():
        return ""
    name = f"reply_{uuid.uuid4().hex[:10]}.aiff"
    path = AUDIO_DIR / name
    system = platform.system()

    try:
        if system == "Darwin" and shutil.which("say"):
            subprocess.run(
                ["say", "-o", str(path), "--", text],
                check=True,
                timeout=120,
            )
            return name

        import pyttsx3
        wav_name = name.replace(".aiff", ".wav")
        wav_path = AUDIO_DIR / wav_name
        engine = pyttsx3.init()
        engine.save_to_file(text, str(wav_path))
        engine.runAndWait()
        return wav_name
    except Exception as exc:
        logger.exception("TTS failed")
        return ""
