# backend/llm.py

import os
import logging
from groq import Groq

logger = logging.getLogger(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ✅ UPDATED: Use currently supported Groq models
# Options:
# - "llama-3.1-8b-instant" (fast, free tier friendly)
# - "llama-3.3-70b-versatile" (more powerful, higher quota usage)
DEFAULT_MODEL = "llama-3.1-8b-instant"

def generate_answer(question: str, context_chunks: list) -> str:
    """Generate answer using Groq LLM based on retrieved context chunks."""
    if not question:
        logger.error("❌ Empty question received")
        return "Error: No question provided"
    
    if not context_chunks or len(context_chunks) == 0:
        logger.error("❌ No context chunks provided")
        return "Error: No context available to generate answer"
    
    context_text = "\n\n".join(chunk for chunk in context_chunks if chunk)
    
    if not context_text.strip():
        logger.error("❌ Context text is empty after joining chunks")
        return "Error: Context is empty"
    
    system_prompt = """You are a helpful assistant that answers questions based ONLY on the provided context.
    
Rules:
1. Use ONLY the information from the context to answer the question.
2. If the answer is not in the context, clearly state that you do not have enough information.
3. Do not make up or hallucinate information.
4. Keep answers concise and relevant.
5. Do not mention the context or documents in your response."""

    user_prompt = f"""Context:
{context_text}

Question:
{question}

Answer:"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    try:
        logger.info(f"🤖 Sending request to Groq (model: {DEFAULT_MODEL})...")
        
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages,
            temperature=0.1,
            max_tokens=1024,
            timeout=30,
            top_p=1,
            stream=False
        )
        
        if response and response.choices and len(response.choices) > 0:
            answer = response.choices[0].message.content.strip()
            logger.info(f"✅ Answer generated ({len(answer)} characters)")
            return answer
        else:
            logger.error("❌ Groq returned empty response")
            return "Error: LLM returned no content"
            
    except Exception as e:
        error_msg = str(e)
        logger.error(f"❌ Groq API error: {error_msg}")
        
        if "api_key" in error_msg.lower() or "401" in error_msg:
            return "Error: Invalid or missing Groq API key"
        elif "timeout" in error_msg.lower():
            return "Error: LLM request timed out"
        elif "rate limit" in error_msg.lower():
            return "Error: Groq rate limit exceeded. Please try again later."
        elif "decommissioned" in error_msg.lower() or "model_decommissioned" in error_msg:
            return "Error: Model has been decommissioned. Update to llama-3.1-8b-instant or llama-3.3-70b-versatile."
        else:
            return f"Error calling Groq LLM: {error_msg}"