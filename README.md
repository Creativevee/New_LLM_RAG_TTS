# Document Q&A — Rakesh build

A focused take on the LLM_TTS_Project: upload a document, ask questions about it,
get a written and spoken answer grounded in the document content.

This branch differs from the team's other branches in scope and stack:

- Real **upload endpoint** for PDF, DOCX, TXT, and MD files (not a hard-coded file).
- **Sentence-aware chunking with overlap** (not fixed 200-char windows).
- Explicit **`sentence-transformers`** embeddings (`all-MiniLM-L6-v2`).
- ChromaDB persistent vector store under `vectors/`.
- **Groq `llama-3.3-70b-versatile`** for grounded answers.
- **gTTS** for lightweight cloud-free local audio generation (MP3, no GPU needed).
- Chat-style frontend with drag-and-drop upload, source chips, and inline audio.

## Project layout

```
backend/
  main.py         # FastAPI app + endpoints
  config.py       # paths, model names, limits
  ingest.py       # file parsing, chunking, indexing
  retriever.py    # vector search
  generator.py    # LLM call (Groq)
  speaker.py      # TTS (gTTS)
  requirements.txt
frontend/
  index.html
  app.js
  styles.css
```

Runtime folders `uploads/`, `audio/`, `vectors/` are created on demand and ignored
by git.

## Setup

```bash
cd backend
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
echo "GROQ_API_KEY=your_key_here" > ../.env
uvicorn main:app --reload --port 8000
```

Then open `frontend/index.html` directly in a browser, or serve it:

```bash
cd frontend
python -m http.server 5173
# visit http://127.0.0.1:5173
```

## API

| Method | Path         | Body / Query                | Description                              |
|--------|--------------|-----------------------------|------------------------------------------|
| GET    | `/health`    | —                           | Liveness + indexed document list         |
| GET    | `/documents` | —                           | List indexed document filenames          |
| POST   | `/upload`    | `multipart/form-data: file` | Upload + index a document                |
| POST   | `/ask`       | `{ question, speak }`       | Retrieve, answer, and (optionally) speak |
| POST   | `/reset`     | —                           | Drop the collection and uploaded files   |

## How it works

1. Upload → file is saved under `uploads/`, parsed, split into sentence-aware
   chunks (~600 chars, 80-char overlap), embedded, stored in ChromaDB.
2. Ask → the question is embedded, top-K most similar chunks retrieved.
3. Answer → chunks + question are sent to Groq with a strict grounding prompt.
4. Speak → answer text is rendered to MP3 via gTTS and served from `/media/`.
