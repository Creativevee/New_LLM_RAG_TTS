import chromadb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "raw_docs" / "company_info.txt"
CHROMA_DIR = BASE_DIR / "data" / "chroma_db"

client = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = client.get_or_create_collection(name="knowledge_base")


def load_document():
    text = DATA_FILE.read_text(encoding="utf-8")
    return text


def split_text(text, chunk_size=200):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        if chunk.strip():
            chunks.append(chunk)
    return chunks


def index_document():
    text = load_document()
    chunks = split_text(text)

    existing = collection.get()
    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    for i, chunk in enumerate(chunks):
        collection.add(
            ids=[f"doc_{i}"],
            documents=[chunk],
            metadatas=[{"source": "company_info.txt"}]
        )


def search_docs(query, n_results=3):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results