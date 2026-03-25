
## Project Overview

This project is a question answering system that combines:

- **LLM** for generating answers
- **RAG** for retrieving relevant information from documents
- **TTS** for converting the final answer into audio

The system works like this:

1. A user asks a question
2. The system searches uploaded documents for relevant information
3. The retrieved content is sent to the LLM
4. The LLM generates an answer based on that content
5. The answer is converted into speech using Qwen TTS
6. The user receives both text and audio output

This project is being developed locally and stored on GitHub for collaboration.

---

## Main Goal

The goal of this project is to build a system that can:

- answer questions using document based knowledge
- reduce hallucination by grounding answers in retrieved context
- convert answers into speech for audio output

---

## Project Structure

```text
llm_tts_project/
│
├── backend/
│   ├── app.py
│   ├── rag.py
│   ├── llm.py
│   ├── tts.py
│   └── requirements.txt
│
├── data/
│   ├── raw_docs/
│   └── chroma_db/
│
├── outputs/
│   └── audio/
│
├── frontend/
│
├── venv/
├── .gitignore
└── README.md
````

### Folder Explanation

* **backend/**
  Contains the main Python files for the API, RAG, LLM, and TTS logic

* **data/raw_docs/**
  Stores the source documents used for retrieval

* **data/chroma_db/**
  Stores the vector database files for retrieval

* **outputs/audio/**
  Stores generated audio files

* **frontend/**
  Optional UI for users to ask questions and play audio

---

## Technologies Used

* Python
* FastAPI
* ChromaDB
* LLM
* Qwen TTS
* GitHub

---

## How the System Works

### Step 1: User asks a question

A user sends a question to the backend API.

### Step 2: RAG searches documents

The system searches indexed documents in the vector database.

### Step 3: Relevant content is retrieved

The most relevant chunks are returned.

### Step 4: LLM generates answer

The retrieved chunks and the user question are passed to the LLM.

### Step 5: TTS converts answer to audio

The final answer is converted into speech and saved as an audio file.

---

## Requirements

Before running this project, make sure you have:

* Python installed
* Git installed
* A working virtual environment
* Required Python packages installed

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Creativevee/LLM_TTS_Project.git
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Mac or Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r backend/requirements.txt
```

If not, install manually:

```bash
pip install fastapi uvicorn chromadb torch transformers accelerate qwen-tts
```

---

## How to Run the Project

### 1. Activate the virtual environment

#### Windows

```bash
venv\Scripts\activate
```

#### Mac or Linux

```bash
source venv/bin/activate
```

### 2. Start the backend

```bash
fastapi dev backend/app.py
```

If that does not work, try:

```bash
uvicorn backend.app:app --reload
```

### 3. Open the API docs

In your browser, open:

```text
http://127.0.0.1:8000/docs
```

From there, you can test the endpoints.

---

## Example API Flow

### Example question

```json
{
  "question": "What does the system do?"
}
```

### Expected flow

* the question is received by the API
* relevant document chunks are retrieved
* the LLM generates an answer
* the answer is passed to TTS
* an audio file is created

---

## Main Backend Files

### `app.py`

This is the main FastAPI entry point.
It receives requests and connects RAG, LLM, and TTS together.

### `rag.py`

Handles:

* loading documents
* chunking text
* indexing into ChromaDB
* searching for relevant chunks

### `llm.py`

Handles:

* preparing the prompt
* sending the prompt to the LLM
* returning the answer

### `tts.py`

Handles:

* taking the answer text
* converting it to speech
* saving the audio file

---


## GitHub Collaboration Guide

This repository uses a protected `main` branch.

### Rules

* do not work directly on `main`
* create your own branch
* push your branch
* open a pull request
* wait for review before merging

### Example branch creation

```bash
git checkout main
git pull origin main
git checkout -b feature/rag
```

### Example save and push

```bash
git add .
git commit -m "Added document retrieval logic"
git push -u origin feature/rag
```

### After pushing

Go to GitHub and open a pull request from your branch into `main`.

---

## Suggested Branch Names

Use clear branch names like:

* `feature/rag`
* `feature/tts`
* `feature/frontend`
* `fix/api-error`

Avoid names like:

* `test`
* `work`
* `update`

---

## Common Problems

### 1. Backend does not start

Check:

* virtual environment is activated
* required packages are installed
* file paths are correct

### 2. Documents are not being retrieved

Check:

* documents exist in `data/raw_docs/`
* indexing ran successfully
* ChromaDB path is correct

### 3. TTS fails

Check:

* model loaded correctly
* device setup is correct
* dependencies are compatible

### 4. Git push fails

Check:

* remote repository is connected
* you have permission
* you are on the correct branch

---

## Future Improvements

Possible next improvements:

* better frontend UI
* support for PDF upload
* improved chunking strategy
* better prompt engineering
* multiple voice options
* deployment to cloud

---

## Contribution Workflow

1. Pull the latest `main`
2. Create a new branch
3. Make changes
4. Commit your work
5. Push your branch
6. Open a pull request
7. Wait for review

---

## Author

Project created and managed by the repository owner.

---

## Final Note

This project is being built in stages:

1. backend setup
2. document retrieval
3. LLM integration
4. TTS integration
5. frontend and team collaboration

The main focus is to get the full pipeline working correctly before improving the UI or adding advanced features.
-----------------------------------------

Below is your content converted into a clean **`README.md` format** that you can directly place in your GitHub repository. I preserved the structure but cleaned the formatting slightly so it renders correctly on GitHub.

You can copy everything below into a file named **`README.md`**.

---

# LLM_TTS_Project - Complete Setup Guide for Beginners

## Project Overview

This project is a **question answering system** that combines three main technologies:

1. **LLM (Large Language Model)** – Generates answers using the Groq Cloud API
2. **RAG (Retrieval Augmented Generation)** – Retrieves relevant information from documents using ChromaDB
3. **TTS (Text-to-Speech)** – Converts the final answer into audio using Qwen TTS

---

## How The System Works

```
Step 1: User asks a question
Step 2: System searches uploaded documents for relevant information (RAG/ChromaDB)
Step 3: Retrieved content is sent to the LLM (Groq Cloud API)
Step 4: LLM generates an answer based on that content
Step 5: Answer is converted into speech using Qwen TTS
Step 6: User receives both text and audio output
```

---

## Main Goal

The goal of this project is to build a system that can:

* Answer questions using **document-based knowledge**
* Reduce hallucination by **grounding answers in retrieved context**
* Convert answers into **speech for audio output**

---

# Important Changes From Original Setup

This guide includes critical updates discovered during development.

| Component            | Original Setup            | Updated Setup                            | Reason                        |
| -------------------- | ------------------------- | ---------------------------------------- | ----------------------------- |
| LLM Provider         | Local Ollama (qwen3.5:9b) | Groq Cloud API (llama-3.3-70b-versatile) | Faster, no local GPU needed   |
| Transformers Version | >=4.35.0                  | ==4.57.3                                 | Required by qwen-tts          |
| Accelerate Version   | >=0.24.0                  | ==1.12.0                                 | Required by qwen-tts          |
| Environment Config   | None                      | `.env + python-dotenv`                   | Secure API key management     |
| System Dependency    | None                      | SoX                                      | Required for audio processing |

---

# Prerequisites

Before starting, ensure you have:

* Python **3.10 or higher**
* Git
* A **Groq API Key** from [https://console.groq.com](https://console.groq.com)
* Linux, macOS, or Windows with WSL

Check installations:

```bash
python3 --version
git --version
```

---

# Step-by-Step Setup Instructions

---

# Step 1: Clone the Repository

```bash
git clone https://github.com/Creativevee/LLM_TTS_Project.git
cd LLM_TTS_Project
```

---

# Step 2: Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

You should see:

```
(venv)
```

at the start of your terminal.

---

# Step 3: Install System Dependencies (SoX)

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install sox libsox-fmt-all -y
```

### macOS

```bash
brew install sox
```

### Windows

1. Download SoX from
   [http://sox.sourceforge.net/](http://sox.sourceforge.net/)

2. Add SoX to your **system PATH**

Verify installation:

```bash
sox --version
```

---

# Step 4: Install Python Dependencies

Navigate to backend:

```bash
cd backend
```

Install dependencies:

```bash
pip install -r requirements.txt
```

⚠️ **Important:** Do NOT run with `--upgrade`.

If versions break:

```bash
pip uninstall transformers accelerate huggingface-hub -y
pip install transformers==4.57.3 accelerate==1.12.0 huggingface-hub==0.36.2
```

---

# Step 5: Configure Environment Variables

Create `.env` in the **project root**.

Project structure:

```
LLM_TTS_Project/
│
├── .env
├── backend/
│   ├── app.py
│   ├── llm.py
│   ├── rag.py
│   ├── tts.py
│   └── requirements.txt
```

---

## Add your Groq API key

Create the file:

```bash
echo "GROQ_API_KEY=gsk_your_actual_key_here" > .env
```

Verify:

```bash
cat .env
```

Add `.env` to `.gitignore`:

```bash
echo ".env" >> .gitignore
```

---

# Step 6: Add Documents for RAG

Place documents inside:

```
data/raw_docs/
```

Example:

```
data/raw_docs/company_info.txt
```

Supported formats:

```
.txt
.md
```

---

# Step 7: Start the Backend Server

Go to backend:

```bash
cd backend
```

Kill old servers:

```bash
pkill -f uvicorn
sleep 2
```

Start server:

```bash
uvicorn app:app --reload
```

Expected output:

```
INFO: Uvicorn running on http://127.0.0.1:8000
```

---

# Step 8: Test the API

Open in browser:

```
http://127.0.0.1:8000/docs
```

Test `/ask` endpoint.

Example request:

```json
{
  "question": "What does the system do?"
}
```

Example response:

```json
{
  "question": "What does the system do?",
  "retrieved_chunks": ["document text..."],
  "answer": "The system answers questions using document-based knowledge...",
  "audio_file": "outputs/audio/answer.wav"
}
```

---

# Step 9: Verify Audio Output

Check file:

```bash
ls outputs/audio/
```

Play audio.

### Linux

```bash
aplay outputs/audio/answer.wav
```

### macOS

```bash
afplay outputs/audio/answer.wav
```

### Windows

```bash
powershell -c (New-Object Media.SoundPlayer "outputs/audio/answer.wav").PlaySync()
```

---

# Requirements.txt

`backend/requirements.txt`

```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0

python-dotenv==1.0.0
requests==2.31.0

groq>=0.4.0

chromadb>=0.4.22

torch>=2.1.0
transformers==4.57.3
accelerate==1.12.0
huggingface-hub==0.36.2

scipy>=1.11.0
numpy>=1.24.0
soundfile>=0.12.0
```

⚠️ Do NOT change:

```
transformers==4.57.3
accelerate==1.12.0
```

---

# Project Structure

```
llm_tts_project/

├── .env
├── .gitignore
├── README.md

├── backend/
│   ├── app.py
│   ├── llm.py
│   ├── rag.py
│   ├── tts.py
│   └── requirements.txt

├── data/
│   ├── raw_docs/
│   └── chroma_db/

├── outputs/
│   └── audio/

├── frontend/

└── venv/
```

---

# Common Errors and Fixes

### Address already in use

```
pkill -f uvicorn
sleep 2
uvicorn app:app --reload
```

---

### ImportError check_model_inputs

Install correct versions:

```
pip uninstall transformers accelerate huggingface-hub -y
pip install transformers==4.57.3 accelerate==1.12.0 huggingface-hub==0.36.2
```

---

### Groq API key error

Check:

```
cat .env
```

Ensure:

```
GROQ_API_KEY=gsk_xxx
```

---

### SoX not found

```
sudo apt install sox libsox-fmt-all
```

Verify:

```
which sox
```

---

# Security Guidelines

### DO

* Store API keys in `.env`
* Add `.env` to `.gitignore`
* Use environment variables in code

### DO NOT

* Commit API keys
* Hardcode keys
* Use `--upgrade` on dependencies

Check before pushing:

```
git status | grep .env
grep -r "gsk_" backend/
```

---

# GitHub Collaboration Workflow

Never work directly on `main`.

Create branch:

```
git checkout main
git pull origin main
git checkout -b feature/rag-improvement
```

Commit:

```
git add .
git commit -m "Added document retrieval logic"
git push -u origin feature/rag-improvement
```

Then open a **Pull Request**.

---

# Suggested Branch Names

Good:

```
feature/rag
feature/tts
feature/frontend
fix/api-error
```

Avoid:

```
test
work
update
```

---

# Future Improvements

| Feature             | Priority |
| ------------------- | -------- |
| Better frontend UI  | High     |
| PDF upload support  | High     |
| Multiple TTS voices | Medium   |
| Cloud deployment    | Medium   |
| Answer caching      | Low      |
| Improved chunking   | Low      |

---

# Final Notes

Key reminders:

* Pin dependency versions
* Never commit `.env`
* Test **RAG → LLM → TTS** pipeline before pushing
* Use clear branch names and PR descriptions

---

Here is the **new section** to add to your `README.md`. This documents all the new features, architectural changes, and technical decisions you've made.

Add this section **after the "Technologies Used" section** and **before the "How the System Works" section**.

---

## 🆕 Recent Updates & Enhancements

### 1. Groq Cloud API Integration (Speed Optimization)
**What Changed:**
- Switched from local Ollama LLM to **Groq Cloud API** for inference
- Updated `backend/llm.py` to use Groq's `llama-3.1-8b-instant` model

**Why:**
- **100x faster** token generation (~100+ tokens/sec vs ~5 tokens/sec locally)
- No local GPU memory requirements for LLM
- Reduces local hardware constraints for team members
- Maintains RAG grounding to prevent hallucination

**Files Modified:**
- `backend/llm.py` - Groq API integration
- `backend/requirements.txt` - Added `groq>=0.4.0`
- `.env` - Added `GROQ_API_KEY` (never commit to Git)

---

### 2. RAG Knowledge Update Endpoint (Up-Training Competency)
**What Changed:**
- Added new endpoint: `POST /update-knowledge`
- Created demo script: `demo_knowledge_update.sh`

**Why:**
- Demonstrates **"up-training" competency** as required by instructor
- Shows RAG-based knowledge updates without model fine-tuning
- Allows dynamic knowledge injection by adding documents to `data/raw_docs/`
- Aligns with instructor's recommendation: *"RAG is a recommended approach for Knowledge Update"*

**Usage:**
```bash
# 1. Add new document
echo "New company info here" > data/raw_docs/new_info.txt

# 2. Re-index knowledge base
curl -X POST http://localhost:8000/update-knowledge

# 3. Ask questions with new knowledge
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the new info?"}'
```

**Files Added:**
- `demo_knowledge_update.sh` - Automated demo script
- `backend/app.py` - Added `/update-knowledge` endpoint

---

### 3. Environment Variable Management (Security)
**What Changed:**
- Added `python-dotenv` for `.env` file support
- API keys now loaded from environment variables, not hardcoded

**Why:**
- **Security:** Prevents API keys from being committed to GitHub
- **Flexibility:** Different keys for development/production
- **Best Practice:** Follows 12-factor app methodology

**Setup:**
```bash
# Create .env file in project root (add to .gitignore)
echo "GROQ_API_KEY=gsk_your_key_here" > .env
```

**Files Modified:**
- `backend/app.py` - Added `load_dotenv()` at startup
- `.gitignore` - Added `.env` to prevent accidental commits
- `backend/requirements.txt` - Added `python-dotenv==1.0.0`

---

### 4. Dependency Version Pinning (Stability)
**What Changed:**
- Pinned exact versions for critical packages
- Removed `--upgrade` flag from installation instructions

**Why:**
- **qwen-tts** requires specific versions: `transformers==4.57.3`, `accelerate==1.12.0`
- Prevents breaking changes from automatic upgrades
- Ensures all team members have identical environments
- Fixes `ImportError: cannot import name 'check_model_inputs'`

**Critical Versions:**
```text
transformers==4.57.3    # Required by qwen-tts
accelerate==1.12.0      # Required by qwen-tts
huggingface-hub==0.36.2 # Compatibility with above
fastapi==0.104.1        # Stable with our middleware
```

**Files Modified:**
- `backend/requirements.txt` - Pinned all critical versions

---

### 5. System Dependencies (TTS Audio Processing)
**What Changed:**
- Added **SoX** (Sound eXchange) as a required system package
- Added installation instructions for Linux/macOS/Windows

**Why:**
- **Qwen-TTS** requires SoX for audio file processing
- Cannot be installed via `pip` (system-level dependency)
- Fixes `/bin/sh: 1: sox: not found` error

**Installation:**
```bash
# Linux (Ubuntu/Debian)
sudo apt install sox libsox-fmt-all

# macOS
brew install sox

# Windows
# Download from: http://sox.sourceforge.net/
```

**Files Modified:**
- `README.md` - Added system dependencies section
- `backend/tts.py` - Added SoX error handling

---

### 6. Hybrid Architecture (Speed + Competency)
**What Changed:**
- **LLM Inference:** Groq Cloud API (for speed)
- **Knowledge Updates:** RAG with ChromaDB (for competency)
- **TTS:** Qwen-TTS local (for audio output)

**Why:**
- Balances **performance** (Groq) with **learning objectives** (RAG up-training)
- Demonstrates understanding of both cloud and local AI deployment
- Production-ready architecture with educational value

**Architecture Diagram:**
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   User      │────▶│  FastAPI    │────▶│   ChromaDB  │
│  Question   │     │   Backend   │     │   (RAG)     │
└─────────────┘     └────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Groq API  │
                    │  (LLM)      │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  Qwen-TTS   │
                    │  (Audio)    │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   User      │
                    │  Audio Out  │
                    └─────────────┘
```

---

### 7. Demo & Portfolio Documentation
**What Changed:**
- Added automated demo script for knowledge updates
- Created portfolio documentation templates
- Recorded before/after knowledge update demonstrations

**Why:**
- Provides **evidence of competency** for instructor evaluation
- Shows understanding of RAG vs fine-tuning tradeoffs
- Makes project presentation easier for team members

**Files Added:**
- `demo_knowledge_update.sh` - Automated demo
- `docs/` - Portfolio documentation folder (optional)

---

## ⚠️ Important Notes for Team Members

### Do NOT Use `--upgrade` Flag
```bash
# ❌ WRONG - This breaks qwen-tts
pip install -r requirements.txt --upgrade

# ✅ CORRECT - Uses pinned versions
pip install -r requirements.txt
```

### Always Check `.env` Before Committing
```bash
# Verify .env is in .gitignore
cat .gitignore | grep .env

# Never commit API keys
git status  # Should NOT show .env
```

### SoX Must Be Installed System-Wide
```bash
# Verify installation
sox --version

# If missing, install before running server
sudo apt install sox libsox-fmt-all
```

---

## 📊 Performance Comparison

| Component | Before (Local Ollama) | After (Groq + RAG) |
|-----------|----------------------|-------------------|
| **LLM Speed** | ~5 tokens/sec | ~100+ tokens/sec |
| **Memory Usage** | 4.7 GB (model loaded) | ~100 MB (API calls only) |
| **Knowledge Update** | Manual re-index | `/update-knowledge` endpoint |
| **Team Accessibility** | GPU required | Any machine with internet |
| **Cost** | Free (local resources) | Free tier (Groq) |

---

## 🔧 Troubleshooting Quick Reference

| Error | Solution |
|-------|----------|
| `ImportError: check_model_inputs` | `pip install transformers==4.57.3` |
| `/bin/sh: 1: sox: not found` | `sudo apt install sox libsox-fmt-all` |
| `Error: Invalid or missing Groq API key` | Check `.env` file exists in project root |
| `Model has been decommissioned` | Update `llm.py` to `llama-3.1-8b-instant` |
| `gradio requires fastapi>=0.115.2` | `pip uninstall gradio` (not needed) |

---

## 📝 For Instructor Evaluation

### Competencies Demonstrated

| Competency | How Demonstrated |
|------------|-----------------|
| **LLM Integration** | Groq API with proper error handling |
| **RAG Implementation** | ChromaDB vector search with context retrieval |
| **Knowledge Update** | `/update-knowledge` endpoint + demo script |
| **TTS Integration** | Qwen-TTS with audio file generation |
| **Security Best Practices** | `.env` files, API key management, `.gitignore` |
| **Dependency Management** | Pinned versions, conflict resolution |
| **System Administration** | SoX installation, virtual environment setup |
| **Git Collaboration** | Branch workflow, PR process, protected main |

### Why RAG Over Fine-Tuning?

We chose RAG for knowledge updates because:

1. **Speed:** Instant re-indexing vs hours of training
2. **Cost:** CPU-only vs expensive GPU training
3. **Flexibility:** Easy to add/remove documents
4. **Auditability:** Can trace answers to source documents
5. **Instructor Recommendation:** Email stated *"RAG is a recommended approach for Knowledge Update"*

We understand fine-tuning techniques (LoRA, adapters) but chose RAG as the optimal solution for this use case.

---
# LLM_TTS_Project - Next Steps Guide

This document explains what happens after you complete the setup in the main README, and walks you through each step of using and extending the project.

---

## What Happens After Setup Is Complete

Once you have:
- Cloned the repository
- Created a virtual environment
- Installed dependencies
- Configured your Groq API key
- Started the backend server

The system is ready to receive questions and generate answers with audio output.

---

## Step 1: Verify the Backend Is Running

### Command
```bash
curl http://127.0.0.1:8000/
```

### What Is Happening
This sends a simple HTTP GET request to your FastAPI backend.

### Expected Response
```json
{
  "status": "online",
  "message": "Backend is working"
}
```

### Why This Matters
This confirms:
- The server is running on port 8000
- FastAPI is responding to requests
- No import errors or crashes occurred on startup

---

## Step 2: Verify Your Groq API Key Is Loaded

### Command
```bash
curl http://127.0.0.1:8000/debug-env
```

### What Is Happening
This endpoint checks if the `GROQ_API_KEY` environment variable is available to the application.

### Expected Response
```json
{
  "GROQ_API_KEY_set": true
}
```

### Why This Matters
If this returns `false`, the LLM calls will fail with an authentication error. This step ensures your `.env` file is being loaded correctly.

---

## Step 3: Add Documents for RAG Retrieval

### Action
Place text files in the `data/raw_docs/` folder:

```
data/raw_docs/
├── company_info.txt
├── product_specs.md
└── faq.txt
```

### What Is Happening
When the backend starts, the `lifespan` function in `app.py` checks if the ChromaDB vector database is empty. If it is, it runs `index_document()` from `rag.py`, which:

1. Reads all files from `data/raw_docs/`
2. Splits the text into chunks (typically 500-1000 characters each)
3. Converts each chunk into a vector embedding using a transformer model
4. Stores the embeddings in ChromaDB for fast similarity search

### Why This Matters
Without documents in `data/raw_docs/`, the RAG system has nothing to search. The LLM will still generate answers, but they will not be grounded in your specific knowledge base.

---

## Step 4: Test the Full Pipeline via API

### Action
Use the `/ask` endpoint with a test question:

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What does the system do?"}'
```

### What Is Happening (Step by Step)

#### 4.1 Request Received
FastAPI receives the POST request and parses the JSON body into a `QuestionRequest` object.

#### 4.2 RAG Search (`rag.py`)
The `search_docs()` function:
- Converts the user question into a vector embedding
- Searches ChromaDB for the most similar document chunks
- Returns the top-k relevant chunks (usually 3-5)

#### 4.3 LLM Generation (`llm.py`)
The `generate_answer()` function:
- Formats a prompt that includes the retrieved chunks and the user question
- Sends the prompt to Groq Cloud API using the `llama-3.3-70b-versatile` model
- Receives the generated answer text
- Returns the answer to the backend

#### 4.4 TTS Conversion (`tts.py`)
The `text_to_speech()` function:
- Takes the answer text
- Loads the Qwen TTS model (if not already loaded)
- Generates audio waveform using the model
- Saves the audio as a `.wav` file in `outputs/audio/`
- Returns the file path

#### 4.5 Response Sent
The backend returns a JSON response containing:
- The original question
- The retrieved document chunks
- The generated answer text
- The path to the audio file

### Expected Response
```json
{
  "question": "What does the system do?",
  "retrieved_chunks": [
    "The system answers questions using document-based knowledge...",
    "It uses RAG to retrieve relevant context..."
  ],
  "answer": "The system answers questions by searching documents and generating grounded responses.",
  "audio_file": "http://127.0.0.1:8000/audio/answer.wav"
}
```

### Why This Matters
This confirms the entire pipeline works:
- RAG finds relevant documents
- LLM generates a coherent answer
- TTS produces playable audio
- The frontend can access the audio via URL

---

## Step 5: Test the Frontend UI

### Action
1. Open a new terminal
2. Navigate to the frontend folder:
   ```bash
   cd frontend
   ```
3. Start a simple HTTP server:
   ```bash
   python -m http.server 3000
   ```
4. Open your browser to:
   ```
   http://127.0.0.1:3000
   ```

### What Is Happening
- The browser loads `index.html`, `style.css`, and `script.js`
- When you type a question and click "Ask", `script.js` sends a POST request to `http://127.0.0.1:8000/ask`
- The response is parsed and displayed:
  - The answer text appears in the answer box
  - The "Play Audio" button becomes visible
- When you click "Play Audio", the browser fetches the audio file from `http://127.0.0.1:8000/audio/answer.wav` and plays it

### Why This Matters
This confirms the frontend can:
- Communicate with the backend API
- Display responses correctly
- Play audio files served by the backend

---

## Step 6: Verify Audio Output

### Action
Check if the audio file was created:

```bash
ls -lh outputs/audio/
```

Play the audio:

**Linux:**
```bash
aplay outputs/audio/answer.wav
```

**macOS:**
```bash
afplay outputs/audio/answer.wav
```

### What Is Happening
The Qwen TTS model generated a waveform from the answer text and saved it as a WAV file using the `soundfile` library. SoX (the system audio tool) may be used internally for format conversion or processing.

### Why This Matters
If the file does not exist or cannot be played, there is an issue with:
- The TTS model loading
- SoX installation
- File permissions or paths

---

## Step 7: Monitor Logs for Errors

### Action
Watch the backend terminal output while testing.

### What to Look For
```
INFO:     POST /ask
🔍 Searching for: What does the system do?
🤖 Sending request to Groq...
✅ Answer generated (120 characters)
🔊 Generating audio with Qwen TTS...
✅ Request completed successfully
```

### Common Error Messages and Meaning

| Error | Likely Cause |
|-------|-------------|
| `ImportError: check_model_inputs` | Wrong transformers version |
| `GroqError: api_key must be set` | `.env` not loaded or key missing |
| `SoX could not be found` | System dependency not installed |
| `Connection refused` | Backend not running or wrong port |
| `404 Not Found` for audio | Audio path not served as static file |

### Why This Matters
Logs provide immediate feedback on which step failed, making debugging faster.

---

## Step 8: Add More Documents and Test Edge Cases

### Action
1. Add a PDF or longer text file to `data/raw_docs/`
2. Delete the ChromaDB folder to force re-indexing:
   ```bash
   rm -rf data/chroma_db/*
   ```
3. Restart the backend
4. Ask a question about the new document

### What Is Happening
- The new document is chunked and embedded
- ChromaDB is rebuilt with the new vectors
- Questions about the new content should now retrieve relevant chunks

### Test Edge Cases
- Ask a question with no answer in the documents (should return "not enough information")
- Ask a very long question
- Ask a question with typos
- Ask the same question twice (to test caching if implemented)

### Why This Matters
Testing edge cases ensures the system is robust and handles real-world usage.

---

## Step 9: Prepare for Team Collaboration

### Action
1. Ensure `.env` is in `.gitignore`
2. Commit your code to a feature branch:
   ```bash
   git checkout -b feature/your-change
   git add .
   git commit -m "Description of change"
   git push -u orig**Last updated:** March 2026
**Repository:** https://github.com/Creativevee/LLM_TTS_Project
**Questions:** Open an issue or contact the repository ownerin feature/your-change
   ```
3. Open a pull request on GitHub

### What Is Happening
- Your changes are isolated in a branch
- Team members can review the code before merging
- The protected `main` branch remains stable

### Why This Matters
Following the collaboration workflow prevents breaking the main codebase and enables code review.

---

## Step 10: Plan for Deployment (Future)

### Options
| Platform | Pros | Cons |
|----------|------|------|
| Hugging Face Spaces | Easy setup, free tier | CPU-only on free tier, ephemeral storage |
| RunPod / Lambda Labs | GPU access, persistent storage | Hourly cost, more setup |
| AWS EC2 / GCP Compute | Full control, scalable | More complex, cost management |

### What Needs to Change for Cloud Deployment
1. **Persistent Storage**: ChromaDB and audio files must survive server restarts
2. **Environment Variables**: API keys must be set via cloud platform secrets
3. **Static File Serving**: The `/audio` endpoint must be configured for the cloud environment
4. **CORS**: Origins must be restricted to your frontend domain
5. **Model Loading**: Large models may need to be downloaded on startup or cached

### Why This Matters
Deployment makes the system accessible to users beyond your local machine, but requires additional configuration for reliability and security.

---

## Summary Checklist

After completing setup, verify each step:

- [ ] Backend responds at `http://127.0.0.1:8000/`
- [ ] Groq API key is loaded (`/debug-env` returns `true`)
- [ ] Documents exist in `data/raw_docs/`
- [ ] ChromaDB is populated (check `data/chroma_db/` has files)
- [ ] `/ask` endpoint returns text and audio URL
- [ ] Audio file exists in `outputs/audio/`
- [ ] Frontend can play audio
- [ ] Logs show no errors during request
- [ ] Code is committed to a feature branch, not `main`
- [ ] `.env` is not tracked by Git

---

## What to Do If Something Fails

1. **Check the backend terminal** for error messages
2. **Run the verification commands** in Steps 1-2
3. **Confirm dependencies** are correct:
   ```bash
   pip show transformers accelerate | grep Version
   ```
4. **Confirm SoX is installed**:
   ```bash
   which sox
   ```
5. **Restart the backend** after making changes:
   ```bash
   pkill -f uvicorn
   uvicorn app:app --reload
   ```

---

## Final Notes

This project is built in stages. The core pipeline (RAG → LLM → TTS) is now functional. The next phases are:

1. Improve the frontend UI
2. Add support for more document types (PDF, DOCX)
3. Implement answer caching to reduce API calls
4. Deploy to a cloud platform for public access

Focus on getting the core pipeline stable before adding new features. Test each change thoroughly, and use the collaboration workflow to keep the codebase maintainable.

---

