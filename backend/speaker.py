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
    name = f"reply_{uuid.uuid4().hex[:10]}.wav"
    path = AUDIO_DIR / name
    system = platform.system()

    try:
        if system == "Darwin" and shutil.which("say"):
            subprocess.run(
                [
                    "say",
                    "--data-format=LEI16@22050",
                    "-o",
                    str(path),
                    "--",
                    text,
                ],
                check=True,
                timeout=120,
            )
            return name

        import pyttsx3
        engine = pyttsx3.init()
        engine.save_to_file(text, str(path))
        engine.runAndWait()
        return name
    except Exception as exc:
        logger.exception("TTS failed")
        return ""
