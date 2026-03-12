# ============================================
# 1. LOAD ENVIRONMENT VARIABLES FIRST
# ============================================
from dotenv import load_dotenv
load_dotenv()

# ============================================
# 2. STANDARD IMPORTS (ALL AT TOP)
# ============================================
import os
import sys
import logging
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # <-- Moved here
from pydantic import BaseModel
from fastapi.concurrency import run_in_threadpool

# ============================================
# 3. FIX IMPORT PATHS
# ============================================
current_file_path = Path(__file__).resolve()
backend_dir = current_file_path.parent
project_root = backend_dir.parent
sys.path.append(str(backend_dir))

# ============================================
# 4. IMPORT LOCAL MODULES
# ============================================
from rag import index_document, search_docs
from llm import generate_answer
from tts import text_to_speech

# ============================================
# 5. CONFIGURE LOGGING
# ============================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================
# 6. DEFINE LIFESPAN
# ============================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting up LLM_TTS_Project...")
    
    # Ensure directories exist
    dirs_to_create = [
        project_root / "data" / "raw_docs",
        project_root / "data" / "chroma_db",
        project_root / "outputs" / "audio"
    ]
    for dir_path in dirs_to_create:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # Index documents if ChromaDB is empty
    chroma_path = project_root / "data" / "chroma_db"
    if not any(chroma_path.iterdir()):
        logger.info("⚠️ ChromaDB empty - indexing...")
        try:
            original_cwd = os.getcwd()
            os.chdir(project_root)
            index_document()
            os.chdir(original_cwd)
        except Exception as e:
            logger.error(f"❌ Indexing failed: {e}")
    yield
    logger.info("🛑 Shutting down...")

# ============================================
# 7. INITIALIZE APP
# ============================================
app = FastAPI(
    title="LLM TTS Project API",
    description="RAG-based Question Answering with Text-to-Speech",
    version="1.0.0",
    lifespan=lifespan
)

# ============================================
# 8. ADD CORS MIDDLEWARE
# ============================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# 9. MOUNT STATIC FILES FOR AUDIO
# ============================================
audio_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", "audio")
os.makedirs(audio_dir, exist_ok=True)
app.mount("/audio", StaticFiles(directory=audio_dir), name="audio")

# ============================================
# 10. PYDANTIC MODELS
# ============================================
class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    question: str
    retrieved_chunks: list
    answer: str
    audio_file: str

# ============================================
# 11. ENDPOINTS
# ============================================
@app.get("/")
async def home():
    return {"status": "online", "message": "Backend is working"}

@app.get("/debug-env")
async def debug_env():
    return {
        "GROQ_API_KEY_set": os.environ.get("GROQ_API_KEY") is not None
    }

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(data: QuestionRequest):
    try:
        # RAG Search
        results = await run_in_threadpool(search_docs, data.question)
        if not results or "documents" not in results:
            raise HTTPException(status_code=500, detail="Failed to retrieve documents")
        
        docs = results.get("documents", [[]])[0]
        if not docs:
            raise HTTPException(status_code=404, detail="No relevant context found")

        # LLM Generation
        answer = await run_in_threadpool(generate_answer, data.question, docs)
        if not answer or answer.startswith("Error"):
            raise HTTPException(status_code=500, detail=f"LLM failed: {answer}")

        # TTS Generation
        audio_file = await run_in_threadpool(text_to_speech, answer)
        if not audio_file:
            raise HTTPException(status_code=500, detail="TTS failed")

        # Convert local path to URL for frontend
        audio_filename = os.path.basename(audio_file)
        audio_url = f"http://127.0.0.1:8000/audio/{audio_filename}"

        return {
            "question": data.question,
            "retrieved_chunks": docs,
            "answer": answer,
            "audio_file": audio_url  # Return URL, not file path
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"💥 Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

# ============================================
# 12. RUN DIRECTLY (Optional)
# ============================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)