import logging
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from config import (
    ALLOWED_EXTENSIONS,
    AUDIO_DIR,
    MAX_UPLOAD_BYTES,
    UPLOAD_DIR,
)
from generator import generate
from ingest import index_file, list_documents, reset_index
from retriever import retrieve
from speaker import synthesize

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rakesh-rag")

app = FastAPI(title="Rakesh RAG Q&A", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/media", StaticFiles(directory=str(AUDIO_DIR)), name="media")


class AskRequest(BaseModel):
    question: str
    speak: bool = True


class SourceHit(BaseModel):
    doc: str
    score: float


class AskResponse(BaseModel):
    answer: str
    sources: List[SourceHit]
    audio_url: Optional[str] = None


@app.get("/health")
def health():
    return {"status": "ok", "documents": list_documents()}


@app.get("/documents")
def documents():
    return {"documents": list_documents()}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    safe_name = Path(file.filename or "").name
    if not safe_name:
        raise HTTPException(400, "Invalid filename")

    suffix = Path(safe_name).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Unsupported file type: {suffix or '(none)'}")

    target = UPLOAD_DIR / safe_name
    written = 0
    with open(target, "wb") as out:
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break
            written += len(chunk)
            if written > MAX_UPLOAD_BYTES:
                target.unlink(missing_ok=True)
                raise HTTPException(413, "File exceeds 20MB limit")
            out.write(chunk)

    try:
        chunks_added = index_file(target, safe_name)
    except Exception as exc:
        logger.exception("Indexing failed")
        raise HTTPException(500, f"Could not index file: {exc}")

    return {"filename": safe_name, "chunks_added": chunks_added}


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    if not req.question.strip():
        raise HTTPException(400, "Question is empty")

    hits = retrieve(req.question)
    if not hits:
        return AskResponse(
            answer="No documents are indexed yet. Please upload one first.",
            sources=[],
            audio_url=None,
        )

    passages = [h["text"] for h in hits]
    text = generate(req.question, passages)
    audio_name = synthesize(text) if req.speak else ""

    return AskResponse(
        answer=text,
        sources=[SourceHit(doc=h["doc"], score=h["score"]) for h in hits],
        audio_url=f"/media/{audio_name}" if audio_name else None,
    )


@app.post("/reset")
def reset():
    reset_index()
    for p in UPLOAD_DIR.iterdir():
        if p.is_file():
            p.unlink()
    return {"status": "cleared"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
