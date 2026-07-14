"""
Multiple LLM Providers Integration
OpenAI, Anthropic, Google Gemini, and Open Source models
"""

import requests
import json
import os
from abc import ABC, abstractmethod
from typing import List, Dict, Optional

# ============================================================================
# Abstract Base Class
# ============================================================================

class LLMProvider(ABC):
    """Base class for all LLM providers"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text from prompt"""
        pass
    
    @abstractmethod
    def chat(self, messages: List[Dict], **kwargs) -> str:
        """Chat with message history"""
        pass

# ============================================================================
# OpenAI
# ============================================================================

class OpenAIProvider(LLMProvider):
    """OpenAI API (GPT-3.5, GPT-4)"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = "https://api.openai.com/v1"
        
        if not self.api_key:
            print("⚠️  OpenAI API key not set. Set OPENAI_API_KEY environment variable")
    
    def generate(self, prompt: str, model: str = "gpt-3.5-turbo", **kwargs) -> str:
        """Generate text using OpenAI"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 500)
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code != 200:
                return f"Error: {response.status_code} - {response.text}"
            
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error: {str(e)}"
    
    def chat(self, messages: List[Dict], model: str = "gpt-3.5-turbo", **kwargs) -> str:
        """Chat with OpenAI"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 1000)
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error: {str(e)}"

# ============================================================================
# Anthropic
# ============================================================================

class AnthropicProvider(LLMProvider):
    """Anthropic API (Claude)"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.base_url = "https://api.anthropic.com/v1"
        
        if not self.api_key:
            print("⚠️  Anthropic API key not set. Set ANTHROPIC_API_KEY environment variable")
    
    def generate(self, prompt: str, model: str = "claude-3-haiku-20240307", **kwargs) -> str:
        """Generate text using Anthropic"""
        
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        payload = {
            "model": model,
            "max_tokens": kwargs.get("max_tokens", 500),
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/messages",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code != 200:
                return f"Error: {response.status_code} - {response.text}"
            
            return response.json()["content"][0]["text"]
        except Exception as e:
            return f"Error: {str(e)}"
    
    def chat(self, messages: List[Dict], model: str = "claude-3-haiku-20240307", **kwargs) -> str:
        """Chat with Anthropic"""
        
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        payload = {
            "model": model,
            "max_tokens": kwargs.get("max_tokens", 1000),
            "messages": messages
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/messages",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            return response.json()["content"][0]["text"]
        except Exception as e:
            return f"Error: {str(e)}"

# ============================================================================
# Google Gemini
# ============================================================================

class GeminiProvider(LLMProvider):
    """Google Gemini API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        
        if not self.api_key:
            print("⚠️  Google API key not set. Set GOOGLE_API_KEY environment variable")
    
    def generate(self, prompt: str, model: str = "gemini-pro", **kwargs) -> str:
        """Generate text using Gemini"""
        
        payload = {
            "contents": {
                "parts": [{"text": prompt}]
            },
            "generationConfig": {
                "temperature": kwargs.get("temperature", 0.7),
                "maxOutputTokens": kwargs.get("max_tokens", 500)
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/models/{model}:generateContent?key={self.api_key}",
                json=payload,
                timeout=30
            )
            
            if response.status_code != 200:
                return f"Error: {response.status_code} - {response.text}"
            
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            return f"Error: {str(e)}"
    
    def chat(self, messages: List[Dict], model: str = "gemini-pro", **kwargs) -> str:
        """Chat with Gemini"""
        
        contents = []
        for msg in messages:
            contents.append({
                "role": "user" if msg["role"] == "user" else "model",
                "parts": [{"text": msg["content"]}]
            })
        
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": kwargs.get("temperature", 0.7),
                "maxOutputTokens": kwargs.get("max_tokens", 1000)
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/models/{model}:generateContent?key={self.api_key}",
                json=payload,
                timeout=30
            )
            
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            return f"Error: {str(e)}"

# ============================================================================
# Open Source (Ollama)
# ============================================================================

class OllamaProvider(LLMProvider):
    """Local open-source models via Ollama"""
    
    def __init__(self):
        self.api_url = "http://localhost:11434/api"
    
    def generate(self, prompt: str, model: str = "llama2", **kwargs) -> str:
        """Generate text using Ollama"""
        
        try:
            response = requests.post(
                f"{self.api_url}/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": kwargs.get("temperature", 0.7)
                    }
                },
                timeout=120
            )
            
            if response.status_code != 200:
                return f"Error: Ollama not responding. Is it running?"
            
            return response.json()["response"]
        except Exception as e:
            return f"Error: {str(e)}"
    
    def chat(self, messages: List[Dict], model: str = "llama2", **kwargs) -> str:
        """Chat with Ollama"""
        
        try:
            response = requests.post(
                f"{self.api_url}/chat",
                json={
                    "model": model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": kwargs.get("temperature", 0.7)
                    }
                },
                timeout=120
            )
            
            return response.json()["message"]["content"]
        except Exception as e:
            return f"Error: {str(e)}"

# ============================================================================
# Unified Interface
# ============================================================================

class UnifiedLLM:
    """Use any provider with same interface"""
    
    PROVIDERS = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "gemini": GeminiProvider,
        "ollama": OllamaProvider
    }
    
    def __init__(self, provider: str, api_key: Optional[str] = None):
        if provider not in self.PROVIDERS:
            raise ValueError(f"Unknown provider: {provider}")
        
        if provider == "ollama":
            self.client = OllamaProvider()
        else:
            self.client = self.PROVIDERS[provider](api_key)
        
        self.provider = provider
    
    def generate(self, prompt: str, model: str = None, **kwargs) -> str:
        """Generate text"""
        return self.client.generate(prompt, model or self._default_model(), **kwargs)
    
    def chat(self, messages: List[Dict], model: str = None, **kwargs) -> str:
        """Chat"""
        return self.client.chat(messages, model or self._default_model(), **kwargs)
    
    def _default_model(self) -> str:
        """Get default model for provider"""
        defaults = {
            "openai": "gpt-3.5-turbo",
            "anthropic": "claude-3-haiku-20240307",
            "gemini": "gemini-pro",
            "ollama": "llama2"
        }
        return defaults[self.provider]

if __name__ == "__main__":
    print("=" * 60)
    print("LLM PROVIDER COMPARISON")
    print("=" * 60)
    
    # Test with Ollama (local, no API key needed)
    print("\n1. OLLAMA (Local, Free)")
    print("-" * 60)
    try:
        ollama = UnifiedLLM("ollama")
        response = ollama.generate("What is machine learning?")
        print(f"Response: {response[:200]}...")
    except Exception as e:
        print(f"Error: {e}")
    
    # Show how to use other providers
    print("\n2. OPENAI (GPT-3.5/4)")
    print("-" * 60)
    print("Example usage:")
    print("""
    openai = UnifiedLLM("openai", api_key="sk-...")
    response = openai.generate("What is machine learning?")
    """)
    
    print("\n3. ANTHROPIC (Claude)")
    print("-" * 60)
    print("Example usage:")
    print("""
    anthropic = UnifiedLLM("anthropic", api_key="sk-ant-...")
    response = anthropic.generate("What is machine learning?")
    """)
    
    print("\n4. GEMINI (Google)")
    print("-" * 60)
    print("Example usage:")
    print("""
    gemini = UnifiedLLM("gemini", api_key="AIza...")
    response = gemini.generate("What is machine learning?")
    """)
    
    print("\n" + "=" * 60)
    print("Setup API keys:")
    print("  export OPENAI_API_KEY='sk-...'")
    print("  export ANTHROPIC_API_KEY='sk-ant-...'")
    print("  export GOOGLE_API_KEY='AIza...'")
