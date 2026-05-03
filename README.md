<<<<<<< HEAD
# Document Q&A — Rakesh build

A focused take on the LLM_TTS_Project: upload a document, ask questions about it,
get a written and spoken answer grounded in the document content.

**No API keys. No external services. Fully local.** Models are downloaded on
first run and cached.

This branch differs from the team's other branches in scope and stack:

- Real **upload endpoint** for PDF, DOCX, TXT, and MD files (not a hard-coded file).
- **Sentence-aware chunking with overlap** (not fixed 200-char windows).
- Explicit **`sentence-transformers`** embeddings (`all-MiniLM-L6-v2`).
- ChromaDB persistent vector store under `vectors/`.
- **Local Hugging Face Transformers** with `Qwen2.5-0.5B-Instruct` for grounded answers.
- **macOS `say`** (with `pyttsx3` fallback on other platforms) for offline audio.
- Chat-style frontend with drag-and-drop upload, source chips, and inline audio.

## Project layout

```
backend/
  main.py         # FastAPI app + endpoints
  config.py       # paths, model names, limits
  ingest.py       # file parsing, chunking, indexing
  retriever.py    # vector search
  generator.py    # local LLM (transformers)
  speaker.py      # offline TTS
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
python3 -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

The first question will trigger downloads of the embedding model (~90 MB) and
the LLM (~1 GB). Subsequent runs are fully offline.

In another terminal, serve the frontend:

```bash
python3 -m http.server 5173 --directory frontend
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
3. Answer → chunks + question are sent to the local Qwen model with a strict
   grounding prompt.
4. Speak → answer text is rendered to AIFF/WAV via the OS speech engine and
   served from `/media/`.

## Configuration

Optional environment variable to swap the LLM:

```bash
export LLM_MODEL="Qwen/Qwen2.5-1.5B-Instruct"   # bigger, better, slower
```

Defaults to `Qwen/Qwen2.5-0.5B-Instruct` for fast CPU inference.
=======
# Hexagon Labs Chatbot

A RAG-powered AI chatbot with Text-to-Speech. Upload a document and ask questions about it, or just chat with the AI directly.

## Features

- Chat with Qwen 2.5 7B via HuggingFace Inference
- Upload documents (PDF, TXT, DOCX, CSV, JSON, MD) for context-aware answers
- Text-to-Speech responses via Edge TTS
- Dark-themed chat UI

## Requirements

- Python 3.10+
- A free [HuggingFace](https://huggingface.co) account and API token

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/Creativevee/New_LLM_RAG_TTS.git
cd New_LLM_RAG_TTS
```

**2. Create a virtual environment and install dependencies**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

**3. Add your API key**

Create a `.env` file in the project root:
```
HF_TOKEN=your_huggingface_token_here
```

Get your token at: https://huggingface.co/settings/tokens

**4. Run the app**
```bash
python main.py
```

Open your browser at: [http://localhost:7860](http://localhost:7860)

## Usage

- Type any question in the chat box and press Enter or click Send
- To use a document: click **Choose File**, select a file, click **Upload**, then ask questions about it
- The bot will read back answers using voice automatically
>>>>>>> db6d43d67722afa8e94bcc962c65ee4199c1f21d
