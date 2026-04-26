import logging
from typing import List

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from config import LLM_MAX_NEW_TOKENS, LLM_MODEL

logger = logging.getLogger(__name__)

_tokenizer = None
_model = None

SYSTEM_PROMPT = (
    "You answer questions strictly using the provided excerpts. "
    "If the answer cannot be found in the excerpts, reply exactly: "
    "\"I couldn't find that in the uploaded documents.\" "
    "Be direct and factual. Do not mention the excerpts or restate the question."
)


def _load():
    global _tokenizer, _model
    if _model is not None:
        return
    logger.info("Loading local LLM: %s", LLM_MODEL)
    _tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)
    _model = AutoModelForCausalLM.from_pretrained(
        LLM_MODEL,
        torch_dtype=torch.float32,
        device_map="cpu",
    )
    _model.eval()
    logger.info("LLM ready.")


def generate(question: str, passages: List[str]) -> str:
    if not passages:
        return "No documents are indexed yet. Please upload one first."

    try:
        _load()
    except Exception as exc:
        logger.exception("Model load failed")
        return f"Could not load local model: {exc}"

    excerpts = "\n\n---\n\n".join(passages)
    user_msg = f"Excerpts:\n{excerpts}\n\nQuestion: {question}"

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_msg},
    ]

    try:
        prompt = _tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        inputs = _tokenizer(prompt, return_tensors="pt").to(_model.device)
        with torch.no_grad():
            output_ids = _model.generate(
                **inputs,
                max_new_tokens=LLM_MAX_NEW_TOKENS,
                do_sample=False,
                temperature=1.0,
                pad_token_id=_tokenizer.eos_token_id,
            )
        new_tokens = output_ids[0][inputs["input_ids"].shape[1]:]
        text = _tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
        return text or "(empty response)"
    except Exception as exc:
        logger.exception("Generation failed")
        return f"Error generating answer: {exc}"
