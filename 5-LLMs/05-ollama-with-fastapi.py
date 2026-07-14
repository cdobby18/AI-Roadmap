"""
Serve Ollama models through FastAPI
Create a REST API wrapper around local LLMs
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json

app = FastAPI(title="Local LLM API")

OLLAMA_API = "http://localhost:11434/api"

class GenerateRequest(BaseModel):
    model: str = "llama2"
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 100

class ChatMessage(BaseModel):
    role: str  # "user", "assistant", "system"
    content: str

class ChatRequest(BaseModel):
    model: str = "llama2"
    messages: list[ChatMessage]
    temperature: float = 0.7

@app.get("/health")
def health():
    """Check if Ollama is running"""
    try:
        response = requests.get(f"{OLLAMA_API}/tags", timeout=2)
        return {"status": "healthy", "ollama": "connected"}
    except:
        return {"status": "unhealthy", "ollama": "disconnected"}

@app.get("/models")
def list_models():
    """List available local models"""
    try:
        response = requests.get(f"{OLLAMA_API}/tags")
        models = response.json().get("models", [])
        return {
            "models": [m["name"] for m in models],
            "count": len(models)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate")
def generate(request: GenerateRequest):
    """Generate text from a prompt"""
    try:
        payload = {
            "model": request.model,
            "prompt": request.prompt,
            "stream": False,
            "options": {
                "temperature": request.temperature,
                "num_predict": request.max_tokens
            }
        }
        
        response = requests.post(f"{OLLAMA_API}/generate", json=payload, timeout=60)
        data = response.json()
        
        return {
            "prompt": request.prompt,
            "response": data.get("response", ""),
            "model": request.model,
            "tokens_generated": data.get("eval_count", 0),
            "temperature": request.temperature
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
def chat(request: ChatRequest):
    """Chat interface"""
    try:
        messages = [
            {"role": m.role, "content": m.content}
            for m in request.messages
        ]
        
        payload = {
            "model": request.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": request.temperature
            }
        }
        
        response = requests.post(f"{OLLAMA_API}/chat", json=payload, timeout=60)
        data = response.json()
        
        return {
            "model": request.model,
            "message": data.get("message", {}),
            "done": data.get("done", True)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("Starting Local LLM API server...")
    print("Available endpoints:")
    print("  GET  /health - Check Ollama connection")
    print("  GET  /models - List available models")
    print("  POST /generate - Generate text")
    print("  POST /chat - Chat interface")
    uvicorn.run(app, host="0.0.0.0", port=8000)
