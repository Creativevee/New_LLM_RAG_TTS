import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = ROOT_DIR / "uploads"
AUDIO_DIR = ROOT_DIR / "audio"
VECTOR_DIR = ROOT_DIR / "vectors"

for _d in (UPLOAD_DIR, AUDIO_DIR, VECTOR_DIR):
    _d.mkdir(parents=True, exist_ok=True)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

EMBED_MODEL = "all-MiniLM-L6-v2"
COLLECTION_NAME = "rakesh_kb"

CHUNK_TARGET_CHARS = 600
CHUNK_OVERLAP_CHARS = 80
TOP_K = 4

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".md", ".docx"}
MAX_UPLOAD_BYTES = 20 * 1024 * 1024
