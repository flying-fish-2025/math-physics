from __future__ import annotations

import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
import httpx
from openai import OpenAI


def _load_env_files() -> None:
    """
    Load environment variables more robustly for Streamlit runtime:
    1) current working directory (.env)
    2) nearest .env discovered by python-dotenv
    """
    cwd_env = Path.cwd() / ".env"
    if cwd_env.exists():
        load_dotenv(dotenv_path=cwd_env, override=False)
    found = find_dotenv(filename=".env", usecwd=True)
    if found:
        load_dotenv(dotenv_path=found, override=False)


def build_openai_compatible_client() -> tuple[OpenAI, str]:
    """
    Build OpenAI-compatible client for hiapi/gemini-style endpoints.
    Reads from environment variables:
    - OPENAI_BASE_URL
    - OPENAI_API_KEY
    - MODEL_PRIMARY
    """
    _load_env_files()
    base_url = os.getenv("OPENAI_BASE_URL", "").strip()
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("MODEL_PRIMARY", "gemini-3-flash-no").strip()

    if not base_url:
        raise ValueError("OPENAI_BASE_URL is required (set in .env or sidebar config).")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required (set in .env or sidebar config).")

    # trust_env=False avoids inheriting unexpected proxy settings on Windows.
    http_client = httpx.Client(timeout=90.0, trust_env=False)
    client = OpenAI(base_url=base_url, api_key=api_key, http_client=http_client, max_retries=2)
    return client, model


def smoke_test_chat(prompt: str = "请只返回数字：2+2 等于几？") -> dict:
    client, model = build_openai_compatible_client()
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )
    text = (resp.choices[0].message.content or "").strip()
    return {"model": model, "response": text}

