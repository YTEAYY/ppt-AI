# app/services/openai_client.py
import os
from typing import Dict, Any, Optional

import openai
from langchain_openai import OpenAI

# API 키가 없으면 더미 모드
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
openai.api_key = OPENAI_API_KEY
OPENAI_MODEL = "gpt-4o"


def get_llm() -> Optional[OpenAI]:
    """LangChain LLM wrapper (GPT‑4o)."""
    if not OPENAI_API_KEY:
        return None
    
    return OpenAI(
        model=OPENAI_MODEL,
        temperature=0.7,
        max_tokens=2000,
        top_p=0.9,
        verbose=True,
    )
