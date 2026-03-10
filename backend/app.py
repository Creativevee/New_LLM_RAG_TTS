from fastapi import FastAPI
from pydantic import BaseModel
from rag import index_document, search_docs
from llm import generate_answer
from tts import text_to_speech

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.on_event("startup")
def startup_event():
    index_document()

@app.get("/")
def home():
    return {"message": "Backend is working"}

@app.post("/ask")
def ask_question(data: QuestionRequest):
    results = search_docs(data.question)
    docs = results.get("documents", [[]])[0]

    answer = generate_answer(data.question, docs)
    audio_file = text_to_speech(answer)

    return {
        "question": data.question,
        "retrieved_chunks": docs,
        "answer": answer,
        "audio_file": audio_file
    }

    