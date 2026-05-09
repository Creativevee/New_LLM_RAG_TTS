import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = ROOT_DIR / "uploads"
AUDIO_DIR = ROOT_DIR / "audio"
VECTOR_DIR = ROOT_DIR / "vectors"
DATA_DIR = ROOT_DIR / "data"

for _d in (UPLOAD_DIR, AUDIO_DIR, VECTOR_DIR, DATA_DIR):
    _d.mkdir(parents=True, exist_ok=True)

CONVO_DB_PATH = DATA_DIR / "conversations.db"

LLM_MODEL = os.environ.get("LLM_MODEL", "Qwen/Qwen2.5-0.5B-Instruct")
LLM_MAX_NEW_TOKENS = 512

EMBED_MODEL = "all-MiniLM-L6-v2"
COLLECTION_NAME = "rakesh_kb"

CHUNK_TARGET_CHARS = 600
CHUNK_OVERLAP_CHARS = 80
TOP_K = 4

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".md", ".docx"}
MAX_UPLOAD_BYTES = 20 * 1024 * 1024
