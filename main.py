# main.py - FastAPI Backend (FINAL FIXED VERSION)
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

# ✅ Import everything needed from rag.py
from rag import (
    index_document,
    search_context,
    get_answer,
    text_to_speech,
    validate_file,
    ALLOWED_EXTENSIONS,
)
from io import BytesIO
import os
import base64

app = FastAPI()


# Serve frontend
@app.get("/", response_class=HTMLResponse)
async def get_frontend():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()


# Upload endpoint
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not validate_file(file.filename):
        return {
            "error": f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        }

    content = await file.read()

    # ✅ Unpack 3 values from index_document
    chunks, time_taken, metadata = index_document(content, file.filename)

    return {
        "message": f"✅ Indexed chunks in {time_taken:.2f}s",
        "metadata": {
            "pages": metadata.get("pages", 0),
            "characters": metadata.get("char_count", 0),
            "type": metadata.get("type", "unknown"),
        },
    }


# Chat endpoint
@app.post("/chat")
async def chat(question: str = Form(...)):
    # 1. Search context
    context = search_context(question)
    if not context:
        context = "No relevant document context found."

    # 2. Get LLM answer
    answer = get_answer(question, context)

    # 3. Generate speech
    audio_bytes = await text_to_speech(answer)

    # Return JSON with text + audio as base64
    audio_b64 = base64.b64encode(audio_bytes).decode()

    return {"text": answer, "audio": f"data:audio/mp3;base64,{audio_b64}"}


# Health check
@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
