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
