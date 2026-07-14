"""
Prompt engineering techniques with local models
- Zero-shot prompting
- Few-shot prompting  
- Chain-of-thought
"""

import requests
import json

OLLAMA_API = "http://localhost:11434/api"

def query_model(model: str, prompt: str) -> str:
    """Send a prompt to Ollama and get response"""
    response = requests.post(
        f"{OLLAMA_API}/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json().get("response", "")

def zero_shot(model: str, task: str) -> str:
    """Zero-shot: Ask directly without examples"""
    prompt = f"Task: {task}\n\nResponse:"
    return query_model(model, prompt)

def few_shot(model: str, task: str, examples: list) -> str:
    """Few-shot: Provide examples before the task"""
    prompt = "Examples:\n"
    for input_text, output_text in examples:
        prompt += f"Input: {input_text}\nOutput: {output_text}\n\n"
    
    prompt += f"Now do this:\nInput: {task}\nOutput:"
    return query_model(model, prompt)

def chain_of_thought(model: str, problem: str) -> str:
    """Chain-of-thought: Ask model to think step by step"""
    prompt = f"{problem}\n\nThink step by step:"
    return query_model(model, prompt)

def system_prompt_chat(model: str, system: str, user_msg: str) -> str:
    """Use system prompt to shape model behavior"""
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_msg}
    ]
    response = requests.post(
        f"{OLLAMA_API}/chat",
        json={"model": model, "messages": messages, "stream": False}
    )
    return response.json()["message"]["content"]

if __name__ == "__main__":
    model = "llama2"
    
    # Zero-shot: directly classify sentiment
    print("=== Zero-Shot ===")
    result = zero_shot(model, "Classify sentiment: 'I love this product!'")
    print(result)
    
    # Few-shot: teach by example
    print("\n=== Few-Shot ===")
    examples = [
        ("'Great movie!'", "Positive"),
        ("'Not good at all'", "Negative"),
        ("'It was okay'", "Neutral")
    ]
    result = few_shot(model, "'Amazing experience!'", examples)
    print(result)
    
    # Chain-of-thought: complex reasoning
    print("\n=== Chain-of-Thought ===")
    result = chain_of_thought(
        model,
        "If Alice has 3 apples and Bob gives her 5 more, "
        "then she gives half to Charlie, how many does Alice have?"
    )
    print(result)
    
    # System prompt: shape behavior
    print("\n=== System Prompt ===")
    result = system_prompt_chat(
        model,
        "You are a Python expert. Explain concepts concisely.",
        "What is a decorator?"
    )
    print(result)
