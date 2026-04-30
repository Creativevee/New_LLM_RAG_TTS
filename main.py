# main.py - FastAPI Backend (FINAL FIXED VERSION)
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from uuid import uuid4

# ✅ Import everything needed from rag.py
from rag import (
    index_document,
    search_context,
    get_all_context,
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
    get_kb_documents,
    remove_document_from_kb,
)
import os
import re
import base64

# Matches questions that want a complete list (members, skills, items, etc.)
_LIST_QUERY_RE = re.compile(
    r'\b(list|all|every|who are|give me|show me|what are)\b.{0,60}'
    r'\b(member|team|people|staff|employee|everyone|developer|engineer|name)\b',
    re.IGNORECASE
)

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
        "message": f"✅ Indexed {chunks} chunks in {time_taken:.2f}s",
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
    # For "list all" style questions fetch every chunk so nothing is missed
    if _LIST_QUERY_RE.search(question):
        context, sources = get_all_context()
    else:
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
    try:
        results = chat_collection.get(where={"session_id": session_id})
    except Exception as e:
        print("Error fetching thread:", e)
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

# Admin page
@app.get("/admin", response_class=HTMLResponse)
async def get_admin():
    with open("admin.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/admin/docs")
async def list_admin_docs():
    return {"documents": get_kb_documents()}

@app.post("/admin/docs/add")
async def add_admin_doc(file: UploadFile = File(...)):
    if not validate_file(file.filename):
        return {"error": f"Unsupported file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"}
    content = await file.read()
    chunks, time_taken, metadata = index_document(content, file.filename)
    return {
        "message": f"✅ Indexed {chunks} chunks in {time_taken:.2f}s",
        "chunks": chunks,
        "source": file.filename,
    }

@app.post("/admin/docs/remove")
async def remove_admin_doc(source: str = Form(...)):
    count = remove_document_from_kb(source)
    return {"message": f"Removed {count} chunk(s) for '{source}'.", "count": count}

# Health check
@app.get("/health")
async def health():
    return {"status": "done"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)

