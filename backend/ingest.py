import re
import uuid
from pathlib import Path
from typing import List

import chromadb
from docx import Document
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

from config import (
    CHUNK_OVERLAP_CHARS,
    CHUNK_TARGET_CHARS,
    COLLECTION_NAME,
    EMBED_MODEL,
    VECTOR_DIR,
)

chroma_client = chromadb.PersistentClient(path=str(VECTOR_DIR))
embedder = SentenceTransformer(EMBED_MODEL)


def get_collection():
    return chroma_client.get_or_create_collection(name=COLLECTION_NAME)


def extract_text(file_path: Path) -> str:
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        reader = PdfReader(str(file_path))
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    if suffix == ".docx":
        doc = Document(str(file_path))
        return "\n".join(p.text for p in doc.paragraphs)
    return file_path.read_text(encoding="utf-8", errors="ignore")


def split_into_chunks(text: str) -> List[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []

    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks: List[str] = []
    buf = ""
    for sent in sentences:
        candidate = (buf + " " + sent).strip() if buf else sent
        if len(candidate) <= CHUNK_TARGET_CHARS:
            buf = candidate
            continue
        if buf:
            chunks.append(buf)
        tail = buf[-CHUNK_OVERLAP_CHARS:] if buf else ""
        buf = (tail + " " + sent).strip()
    if buf:
        chunks.append(buf)
    return chunks


def index_file(file_path: Path, doc_label: str) -> int:
    text = extract_text(file_path)
    chunks = split_into_chunks(text)
    if not chunks:
        return 0

    coll = get_collection()
    embeddings = embedder.encode(chunks).tolist()
    batch_id = uuid.uuid4().hex[:8]
    ids = [f"{doc_label}::{batch_id}::{i}" for i in range(len(chunks))]
    metadatas = [{"doc": doc_label, "chunk_index": i} for i in range(len(chunks))]

    coll.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas,
    )
    return len(chunks)


def list_documents() -> List[str]:
    coll = get_collection()
    data = coll.get()
    metas = data.get("metadatas") or []
    return sorted({m.get("doc", "") for m in metas if m.get("doc")})


def reset_index() -> None:
    try:
        chroma_client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
