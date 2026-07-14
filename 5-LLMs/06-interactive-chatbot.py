"""
Interactive chatbot with Ollama
Talk to local LLMs in real-time
"""

import requests
import json

OLLAMA_API = "http://localhost:11434/api"

class LocalChatBot:
    def __init__(self, model: str = None):
        """Initialize chatbot with a model"""
        # Auto-detect available model if not specified
        if model is None:
            models = self.get_available_models()
            if not models:
                raise Exception("No models found. Run: ollama pull llama2")
            model = models[0]
        
        self.model = model
        self.conversation = []  # Keep conversation history
        print(f"✓ Connected to {model}")
    
    def get_available_models(self):
        """Get list of available models"""
        try:
            response = requests.get(f"{OLLAMA_API}/tags", timeout=5)
            models = response.json().get("models", [])
            return [m["name"] for m in models]
        except:
            return []
    
    def chat(self, user_message: str) -> str:
        """Send message and get response"""
        # Add to conversation history
        self.conversation.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            payload = {
                "model": self.model,
                "messages": self.conversation,
                "stream": False
            }
            
            response = requests.post(
                f"{OLLAMA_API}/chat",
                json=payload,
                timeout=120
            )
            
            if response.status_code != 200:
                return f"Error: {response.status_code} - {response.text}"
            
            data = response.json()
            
            if "error" in data:
                return f"Model error: {data['error']}"
            
            if "message" not in data:
                return f"Unexpected response format: {data}"
            
            assistant_message = data["message"]["content"]
            
            # Add to history
            self.conversation.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except requests.exceptions.Timeout:
            return "⏱️  Request timed out (model is slow). Try a shorter question."
        except requests.exceptions.ConnectionError:
            return "❌ Cannot connect to Ollama. Is it running? (ollama serve)"
        except Exception as e:
            return f"Error: {e}"
    
    def clear_history(self):
        """Reset conversation"""
        self.conversation = []
        print("📝 Conversation cleared")
    
    def show_history(self):
        """Show conversation history"""
        if not self.conversation:
            print("(empty)")
            return
        
        for msg in self.conversation:
            role = "You" if msg["role"] == "user" else "Bot"
            print(f"{role}: {msg['content'][:100]}...")

def main():
    print("=" * 60)
    print("🤖 LOCAL CHATBOT WITH OLLAMA")
    print("=" * 60)
    
    # Initialize bot
    try:
        bot = LocalChatBot()
    except Exception as e:
        print(f"Error: {e}")
        print("\nSetup:")
        print("1. ollama serve          (in terminal 1)")
        print("2. ollama pull llama2    (in terminal 2)")
        print("3. Run this script again")
        return
    
    print(f"\nModel: {bot.model}")
    print("\nCommands:")
    print("  /history - Show conversation")
    print("  /clear   - Clear conversation")
    print("  /exit    - Quit")
    print("\nStart chatting (Ctrl+C to exit):\n")
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() == "/exit":
                print("Goodbye! 👋")
                break
            elif user_input.lower() == "/history":
                print("\n--- Conversation History ---")
                bot.show_history()
                print()
                continue
            elif user_input.lower() == "/clear":
                bot.clear_history()
                continue
            
            # Get response
            print("\nBot: ", end="", flush=True)
            response = bot.chat(user_input)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    main()
