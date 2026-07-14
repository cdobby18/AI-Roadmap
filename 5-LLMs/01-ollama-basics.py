"""
Basic Ollama integration with Python
Run models locally without API keys
"""

import requests
import json

OLLAMA_API = "http://localhost:11434/api"

def list_models():
    """List all available local models"""
    try:
        response = requests.get(f"{OLLAMA_API}/tags", timeout=5)
        response.raise_for_status()
        models = response.json().get("models", [])
        return [m["name"] for m in models]
    except requests.exceptions.ConnectionError:
        raise Exception("Cannot connect to Ollama. Is it running? Try: ollama serve")
    except Exception as e:
        raise Exception(f"Error listing models: {e}")

def generate_text(model: str, prompt: str, stream: bool = False):
    """Generate text using a local model"""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream
    }
    
    try:
        response = requests.post(f"{OLLAMA_API}/generate", json=payload, stream=stream, timeout=120)
        response.raise_for_status()
        
        if stream:
            # Process streaming response
            full_response = ""
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    full_response += data.get("response", "")
            return full_response
        else:
            return response.json().get("response", "")
    except requests.exceptions.Timeout:
        raise Exception(f"Request timed out. Model may be slow or stuck.")
    except requests.exceptions.ConnectionError:
        raise Exception(f"Cannot connect to Ollama. Is it running?")
    except Exception as e:
        raise Exception(f"Error generating text: {e}")

def chat(model: str, messages: list):
    """Chat interface (like OpenAI's API)"""
    payload = {
        "model": model,
        "messages": messages,
        "stream": False
    }
    
    try:
        response = requests.post(f"{OLLAMA_API}/chat", json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        
        # Check for errors
        if "error" in data:
            raise Exception(f"Ollama error: {data['error']}")
        
        if "message" not in data:
            print(f"DEBUG - Response structure: {data}")
            raise KeyError(f"Expected 'message' in response, got: {list(data.keys())}")
        
        return data["message"]["content"]
    except requests.exceptions.Timeout:
        raise Exception(f"Request timed out. Model may be slow or stuck.")
    except requests.exceptions.ConnectionError:
        raise Exception(f"Cannot connect to Ollama. Is it running?")
    except Exception as e:
        raise Exception(f"Error in chat: {e}")

if __name__ == "__main__":
    # List available models
    try:
        available_models = list_models()
        print("Available models:", available_models)
        
        if not available_models:
            print("\nNo models installed!")
            print("Install one with: ollama pull llama2")
            exit(1)
        
        # Use the first available model
        model = available_models[0]
        print(f"\nUsing model: {model}")
        
    except Exception as e:
        print(f"Error listing models: {e}")
        print("Make sure Ollama is running: ollama serve")
        exit(1)
    
    # Simple generation
    try:
        print("\n--- Testing Generation ---")
        result = generate_text(model, "Write a short Python function that checks if a number is prime:")
        print("Generated Code:")
        print(result[:200] + "..." if len(result) > 200 else result)
    except Exception as e:
        print(f"Generation error: {e}")
    
    # Chat interface
    try:
        print("\n--- Testing Chat ---")
        messages = [
            {"role": "user", "content": "What's the capital of France?"}
        ]
        chat_result = chat(model, messages)
        print("Chat Response:")
        print(chat_result[:200] + "..." if len(chat_result) > 200 else chat_result)
    except Exception as e:
        print(f"Chat error: {e}")
        print("\nTroubleshooting:")
        print("1. Is Ollama running? Try: ollama serve")
        print("2. Do you have models installed? Try: ollama pull llama2")
        print("3. Check model name is correct (not with :latest suffix)")
