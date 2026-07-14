"""
Context Engineering with LLMs
Manage token limits, context windows, and optimize input/output
"""

import requests
import json
from typing import List, Dict

OLLAMA_API = "http://localhost:11434/api"

class TokenCounter:
    """Approximate token counting (most models use ~4 chars = 1 token)"""
    
    @staticmethod
    def count_tokens(text: str) -> int:
        """Rough token count (actual varies by model)"""
        # Most models use ~1 token per 4 characters
        return len(text) // 4
    
    @staticmethod
    def count_messages(messages: List[Dict]) -> int:
        """Count tokens in message list"""
        total = 0
        for msg in messages:
            total += TokenCounter.count_tokens(msg.get("content", ""))
            total += TokenCounter.count_tokens(msg.get("role", ""))
        return total + len(messages) * 4  # Add overhead per message
    
    @staticmethod
    def estimate_response_tokens(max_response: int) -> int:
        """Estimate response token count"""
        return max_response

class ContextManager:
    """Manage context window and optimize token usage"""
    
    # Model context windows (tokens)
    CONTEXT_WINDOWS = {
        "llama2": 4096,
        "mistral": 8192,
        "neural-chat": 4096,
        "orca-mini": 3900,
        "dolphin-mixtral": 32768,
    }
    
    # Reserve tokens for response
    RESPONSE_RESERVE = 500
    
    def __init__(self, model: str):
        self.model = model
        self.context_window = self.CONTEXT_WINDOWS.get(
            model.split(":")[0],  # Remove :latest suffix
            4096  # Default
        )
        self.available_tokens = self.context_window - self.RESPONSE_RESERVE
    
    def get_available_tokens(self, messages: List[Dict]) -> int:
        """Calculate available tokens for new input"""
        used = TokenCounter.count_messages(messages)
        return max(self.available_tokens - used, 100)
    
    def truncate_messages(self, messages: List[Dict], max_tokens: int) -> List[Dict]:
        """Keep only recent messages that fit within token limit"""
        result = []
        token_count = 0
        
        # Always keep system message if present
        if messages and messages[0].get("role") == "system":
            result.append(messages[0])
            token_count += TokenCounter.count_tokens(messages[0].get("content", ""))
        
        # Add messages from newest to oldest
        for msg in reversed(messages[1:] if messages and messages[0].get("role") == "system" else messages):
            msg_tokens = TokenCounter.count_tokens(msg.get("content", ""))
            if token_count + msg_tokens <= max_tokens:
                result.insert(0 if not result or result[0].get("role") != "system" else 1, msg)
                token_count += msg_tokens
            else:
                break
        
        return result
    
    def summarize_old_messages(self, model: str, messages: List[Dict]) -> str:
        """Use LLM to summarize old conversation"""
        conversation_text = "\n".join([
            f"{m['role']}: {m['content']}" for m in messages[:-2]
        ])
        
        prompt = f"""Summarize this conversation in 2-3 sentences:

{conversation_text}"""
        
        response = requests.post(
            f"{OLLAMA_API}/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        
        return response.json().get("response", "")
    
    def optimize_context(self, model: str, messages: List[Dict]) -> List[Dict]:
        """
        Optimize messages for context window
        If too large: summarize old messages
        """
        current_tokens = TokenCounter.count_messages(messages)
        
        if current_tokens <= self.available_tokens:
            return messages
        
        print(f"⚠️  Context too large ({current_tokens} tokens, limit: {self.available_tokens})")
        print("   Optimizing...")
        
        # Try truncating first
        optimized = self.truncate_messages(messages, self.available_tokens - 200)
        
        if TokenCounter.count_messages(optimized) <= self.available_tokens:
            print(f"✓ Truncated to {TokenCounter.count_messages(optimized)} tokens")
            return optimized
        
        # If still too large, summarize
        summary = self.summarize_old_messages(model, messages)
        
        optimized_messages = [
            {"role": "system", "content": f"Previous context: {summary}"},
            messages[-2],  # Keep last user message
            messages[-1]   # Keep last assistant message
        ]
        
        final_tokens = TokenCounter.count_messages(optimized_messages)
        print(f"✓ Summarized and truncated to {final_tokens} tokens")
        
        return optimized_messages

def demo_context_management():
    """Demonstrate context management"""
    
    response = requests.get(f"{OLLAMA_API}/tags")
    models = [m["name"] for m in response.json().get("models", [])]
    
    if not models:
        print("No models. Run: ollama pull llama2")
        return
    
    model = models[0]
    print(f"Using model: {model}")
    print()
    
    # Check context window
    cm = ContextManager(model)
    print(f"Context window: {cm.context_window} tokens")
    print(f"Available for input: {cm.available_tokens} tokens")
    print()
    
    # Create a large message set
    messages = [
        {"role": "system", "content": "You are a helpful Python expert. Keep responses concise."},
        {"role": "user", "content": "What's a decorator in Python?"},
        {"role": "assistant", "content": "A decorator is a function that modifies another function or class..."},
        {"role": "user", "content": "Give me an example"},
        {"role": "assistant", "content": "def my_decorator(func): def wrapper(): print('Before') func() print('After') return wrapper..."},
        {"role": "user", "content": "How about for classes?"},
        {"role": "assistant", "content": "Class decorators work similarly..."},
    ]
    
    # Add large messages to simulate long conversation
    for i in range(10):
        messages.append({"role": "user", "content": f"Question {i}: " + "x" * 500})
        messages.append({"role": "assistant", "content": f"Answer {i}: " + "y" * 500})
    
    print(f"Conversation size: {TokenCounter.count_messages(messages)} tokens")
    print(f"Available space: {cm.available_tokens} tokens")
    
    # Optimize
    optimized = cm.optimize_context(model, messages)
    
    print(f"\nOptimized size: {TokenCounter.count_messages(optimized)} tokens")
    print(f"Messages kept: {len(optimized)}")
    
    # Show what was kept
    print("\nKept messages:")
    for msg in optimized:
        content_preview = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
        print(f"  {msg['role']}: {content_preview}")

if __name__ == "__main__":
    demo_context_management()
