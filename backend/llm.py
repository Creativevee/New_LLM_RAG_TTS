import requests

def generate_answer(question, context_chunks):
    context_text = "\n".join(context_chunks)

    prompt = f"""
Answer the user's question using only the context below.

Context:
{context_text}

Question:
{question}

If the answer is not in the context, say you do not have enough information.
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5:1.5b",
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        if response.status_code != 200:
            return f"Ollama error: {response.status_code} - {response.text}"

        result = response.json()
        return result["response"]

    except Exception as e:
        return f"Error calling Llama: {str(e)}"