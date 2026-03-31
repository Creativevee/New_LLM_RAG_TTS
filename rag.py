# rag.py - Fully Optimized Version
import os
import re
import time
from pathlib import Path
from huggingface_hub import InferenceClient
from pypdf import PdfReader
from io import BytesIO
import chromadb
from chromadb.utils import embedding_functions
import edge_tts
import tempfile
import json
import csv

# --- CONFIG ---
from dotenv import load_dotenv
load_dotenv()
HF_TOKEN = os.environ.get("HF_TOKEN", "")
MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"
VOICE = "en-US-GuyNeural"
ALLOWED_EXTENSIONS = {'.pdf', '.txt', '.docx', '.csv', '.json', '.md'}

# Initialize
client = InferenceClient(token=HF_TOKEN)
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="knowledge_base")

# --- TEXT CLEANING ---
def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s.,!?;:()\-]', '', text)
    text = re.sub(r'\d+\s*/\s*\d+', '', text)
    text = text.strip()
    return text

# --- DOCUMENT LOADERS ---
def load_pdf(path):
    reader = PdfReader(path)
    text = ""
    for i, page in enumerate(reader.pages):
        page_text = page.extract_text()
        if page_text:
            text += f"\n\n[PAGE {i+1}]\n{page_text}"
    return text, {"source": path.name, "pages": len(reader.pages), "type": ".pdf"}

def load_docx(path):
    from docx import Document
    doc = Document(path)
    text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    return text, {"source": path.name, "pages": len(doc.paragraphs), "type": ".docx"}

def load_txt(path):
    encodings = ['utf-8', 'latin-1', 'cp1252']
    for enc in encodings:
        try:
            text = path.read_text(encoding=enc)
            return text, {"source": path.name, "pages": 1, "type": ".txt"}
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Could not decode {path.name}")

def load_csv(path):
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
        text = "\n".join([", ".join(row) for row in rows])
    return text, {"source": path.name, "pages": len(rows), "type": ".csv"}

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        text = json.dumps(data, indent=2)
    return text, {"source": path.name, "pages": 1, "type": ".json"}

def load_document(file_path):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File {file_path} not found")

    loaders = {
        '.pdf': load_pdf,
        '.txt': load_txt,
        '.md': load_txt,
        '.docx': load_docx,
        '.csv': load_csv,
        '.json': load_json
    }

    suffix = path.suffix.lower()
    if suffix not in loaders:
        raise ValueError(f"Unsupported file type: {suffix}")

    text, metadata = loaders[suffix](path)
    text = clean_text(text)
    metadata["char_count"] = len(text)
    return text, metadata

def validate_file(filename: str) -> bool:
    ext = Path(filename).suffix.lower()
    return ext in ALLOWED_EXTENSIONS

# --- SMART CHUNKING ---
def split_text(text, chunk_size=500, chunk_overlap=50):
    chunks = []
    paragraphs = re.split(r'\n\s*\n', text)
    current_chunk = ""
    for para in paragraphs:
        if len(current_chunk) + len(para) < chunk_size:
            current_chunk += "\n" + para
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = para
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

# --- INDEXING ---
def index_document(file_content: bytes, filename: str):
    start_time = time.time()

    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(filename).suffix) as tmp:
        tmp.write(file_content)
        tmp_path = tmp.name

    try:
        text, metadata = load_document(tmp_path)
        chunks = split_text(text)

        try:
            existing = collection.get()
            if existing["ids"]:
                collection.delete(ids=existing["ids"])
        except:
            pass

        batch_size = 50
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            collection.add(
                ids=[f"chunk_{i+j}" for j in range(len(batch))],
                documents=batch,
                metadatas=[metadata for _ in batch]
            )

        elapsed = time.time() - start_time
        return len(chunks), elapsed, metadata
    finally:
        import os
        os.unlink(tmp_path)

# --- SEARCH ---
def search_context(query, n_results=5):
    results = collection.query(query_texts=[query], n_results=n_results)
    if results["documents"][0]:
        return "\n\n".join(results["documents"][0])
    return ""

# --- LLM ---
def get_answer(question, context):
    has_context = bool(context and context.strip() and context != "No relevant document context found.")
    if has_context:
        system_prompt = (
            "You are a helpful AI assistant. A document has been uploaded for reference. "
            "If the question relates to the document, use the provided context to answer. "
            "If the question is general or unrelated to the document, answer from your own knowledge. "
            "Keep answers clear and concise — 2 to 4 sentences. Do not over-explain."
        )
        user_content = f"DOCUMENT CONTEXT:\n{context}\n\nQUESTION: {question}\n\nANSWER:"
    else:
        system_prompt = (
            "You are a helpful AI assistant. Answer any question the user asks clearly and concisely. "
            "Keep answers 2 to 4 sentences — informative but not overly detailed."
        )
        user_content = question

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content}
    ]
    try:
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=messages,
            max_tokens=150,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# --- TTS ---
async def text_to_speech(text):
    audio_data = b""
    communicate = edge_tts.Communicate(text, VOICE)
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return audio_data
