# main.py - FastAPI Backend (FINAL FIXED VERSION)
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from uuid import uuid4

# ✅ Import everything needed from rag.py
from rag import (
    index_document,
    search_context,
    get_answer,
    text_to_speech,
    validate_file,
    ALLOWED_EXTENSIONS,
    get_recent_chat_history,
    store_chat_message,
    chat_collection,
    create_thread,
    get_thread_list,
    reset_thread_messages,
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

#keeping context of the chat
@app.post("/chat")
async def chat(question: str = Form(...), session_id: str = Form(...)):
    #retrieving recent chat history
    history_items = get_recent_chat_history(session_id, limit=10)
    history_text = "\n".join([
        f"{item['role'].upper()}: {item['text']}"
        for item in history_items
    ])
    sources = []
    #answering based on context
    context, sources = search_context(question)
    if not context:
        context = "No relevant document context found."
    answer = get_answer(question, context, history=history_text)
    if not answer or not isinstance(answer, str):
        answer = "Sorry, the assistant could not generate a response."
    store_chat_message(session_id, "user", question)
    store_chat_message(session_id, "assistant", answer)
    audio_bytes = await text_to_speech(answer)
    audio_b64 = base64.b64encode(audio_bytes).decode()
    return {"text": answer, "audio": f"data:audio/mp3;base64,{audio_b64}", "sources": sources}

#creating a new thread
@app.post("/new_thread")
async def new_thread(title: str = Form("Untitled")):
    session_id = str(uuid4())
    create_thread(session_id, title)
    return {"session_id": session_id, "title": title}

#adding API endpoint for threads
@app.get("/threads")
async def threads():
    thread_list = get_thread_list()
    return {"threads": thread_list}  

@app.get("/thread/{session_id}")
async def get_thread_messages(session_id: str):
    results = chat_collection.get(
        where={"session_id": session_id}
    )
    try:
        print("=== DEBUG: fetching thread ===")
        print("session_id:", session_id)
        results = chat_collection.get(where={"session_id": session_id})
        print("results keys:", results.keys())
        print("results count:", len(results["documents"]) if results["documents"] else 0)
        print("sample metadata:", results["metadatas"][0] if results["metadatas"] else "<empty>")
    except Exception as e:
        print("Error:", e)
        return {"messages": []}
    if not results or not results["documents"]:
        return {"messages": []}
    messages = [
        {"role": m["role"], "text": d}
        for d, m in zip(results["documents"], results["metadatas"])
        if m.get("type") != "thread_meta"
    ]
    return {"messages": messages}      


@app.post("/thread/{session_id}/reset")
async def reset_thread(session_id: str):
    deleted_count = reset_thread_messages(session_id)
    return {"message": "Chat reset successfully.", "deleted_messages": deleted_count}

# Health check
@app.get("/health")
async def health():
    return {"status": "done"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)

