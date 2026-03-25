
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
