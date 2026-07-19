"""Simple Ollama client wrapper for local LLM integration.

This file shows how a RAG pipeline can be connected to a local model running
through Ollama on localhost:11434.
"""

import requests


def generate_with_ollama(prompt: str, model: str = "llama2", temperature: float = 0.0) -> str:
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
        },
    }

    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        return response.json().get("response", "")
    except requests.RequestException as exc:
        return f"Ollama call failed: {exc}. Make sure Ollama is running."
