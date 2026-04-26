import logging
from typing import List

from groq import Groq

from config import GROQ_API_KEY, GROQ_MODEL

logger = logging.getLogger(__name__)
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

SYSTEM_PROMPT = (
    "You answer questions strictly using the provided excerpts. "
    "If the answer cannot be found in the excerpts, reply exactly: "
    "\"I couldn't find that in the uploaded documents.\" "
    "Be direct and factual. Do not mention the excerpts or restate the question."
)


def generate(question: str, passages: List[str]) -> str:
    if client is None:
        return "Server is missing GROQ_API_KEY. Set it in a .env file in the project root."
    if not passages:
        return "No documents are indexed yet. Please upload one first."

    excerpts = "\n\n---\n\n".join(passages)
    user_msg = f"Excerpts:\n{excerpts}\n\nQuestion: {question}"

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.2,
            max_tokens=700,
        )
        return response.choices[0].message.content.strip()
    except Exception as exc:
        logger.exception("Groq call failed")
        return f"Error from language model: {exc}"
