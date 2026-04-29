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
from conversations import (
    add_message,
    conversation_exists,
    conversation_message_count,
    create_conversation,
    delete_conversation,
    get_conversation,
    list_conversations,
    make_title,
    rename_conversation,
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
    conversation_id: Optional[str] = None


class SourceHit(BaseModel):
    doc: str
    score: float


class AskResponse(BaseModel):
    answer: str
    sources: List[SourceHit]
    audio_url: Optional[str] = None
    conversation_id: str
    conversation_title: str


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


@app.get("/conversations")
def conversations_index():
    return {"conversations": list_conversations()}


class NewConversationRequest(BaseModel):
    title: Optional[str] = None


@app.post("/conversations")
def conversations_new(payload: Optional[NewConversationRequest] = None):
    title = (payload.title if payload else None) or "New conversation"
    return create_conversation(title)


@app.get("/conversations/{conversation_id}")
def conversations_get(conversation_id: str):
    conv = get_conversation(conversation_id)
    if not conv:
        raise HTTPException(404, "Conversation not found")
    return conv


class RenameRequest(BaseModel):
    title: str


@app.patch("/conversations/{conversation_id}")
def conversations_rename(conversation_id: str, payload: RenameRequest):
    if not rename_conversation(conversation_id, payload.title):
        raise HTTPException(404, "Conversation not found")
    return {"status": "ok"}


@app.delete("/conversations/{conversation_id}")
def conversations_delete(conversation_id: str):
    if not delete_conversation(conversation_id):
        raise HTTPException(404, "Conversation not found")
    return {"status": "deleted"}


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    question = req.question.strip()
    if not question:
        raise HTTPException(400, "Question is empty")

    cid = req.conversation_id
    if not cid or not conversation_exists(cid):
        cid = create_conversation(make_title(question))["id"]
    elif conversation_message_count(cid) == 0:
        rename_conversation(cid, make_title(question))

    hits = retrieve(question)
    if not hits:
        answer = "No documents are indexed yet. Please upload one first."
        add_message(cid, "user", question)
        add_message(cid, "assistant", answer)
        conv = get_conversation(cid)
        return AskResponse(
            answer=answer,
            sources=[],
            audio_url=None,
            conversation_id=cid,
            conversation_title=conv["title"] if conv else make_title(question),
        )

    passages = [h["text"] for h in hits]
    text = generate(question, passages)
    audio_name = synthesize(text) if req.speak else ""
    audio_url = f"/media/{audio_name}" if audio_name else None
    sources = [{"doc": h["doc"], "score": h["score"]} for h in hits]

    add_message(cid, "user", question)
    add_message(cid, "assistant", text, sources=sources, audio_url=audio_url)
    conv = get_conversation(cid)

    return AskResponse(
        answer=text,
        sources=[SourceHit(**s) for s in sources],
        audio_url=audio_url,
        conversation_id=cid,
        conversation_title=conv["title"] if conv else make_title(question),
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
