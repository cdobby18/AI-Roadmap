"""
Compare different models and parameters
Measure latency, token usage patterns, quality
"""

import requests
import json
import time

OLLAMA_API = "http://localhost:11434/api"

def query_with_metrics(model: str, prompt: str, temperature: float = 0.7) -> dict:
    """
    Query model and measure performance metrics
    
    Args:
        model: Model name (llama2, mistral, neural-chat, etc)
        prompt: Input prompt
        temperature: Controls randomness (0=deterministic, 1=creative)
    """
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": 100  # Limit output length for fair comparison
        }
    }
    
    start_time = time.time()
    response = requests.post(f"{OLLAMA_API}/generate", json=payload)
    elapsed = time.time() - start_time
    
    data = response.json()
    
    return {
        "model": model,
        "temperature": temperature,
        "response": data.get("response", ""),
        "latency_seconds": elapsed,
        "tokens_generated": data.get("eval_count", 0),
        "tokens_per_second": data.get("eval_count", 0) / max(elapsed, 0.001),
        "prompt_eval_count": data.get("prompt_eval_count", 0)
    }

def compare_models(prompt: str, models: list = None):
    """Compare multiple models on the same prompt"""
    if models is None:
        models = ["llama2"]  # Add more as you install them
    
    results = []
    for model in models:
        print(f"Testing {model}...")
        try:
            result = query_with_metrics(model, prompt, temperature=0.7)
            results.append(result)
        except Exception as e:
            print(f"  Error: {e}")
    
    # Print comparison
    print("\n" + "="*80)
    print("MODEL COMPARISON")
    print("="*80)
    for r in results:
        print(f"\nModel: {r['model']}")
        print(f"  Latency: {r['latency_seconds']:.2f}s")
        print(f"  Tokens generated: {r['tokens_generated']}")
        print(f"  Tokens/sec: {r['tokens_per_second']:.1f}")
        print(f"  Response: {r['response'][:100]}...")

def test_temperature_effect(model: str, prompt: str):
    """Show how temperature affects output"""
    print(f"\nTesting temperature effects on {model}...")
    print("="*80)
    
    temperatures = [0, 0.3, 0.7, 1.0]
    
    for temp in temperatures:
        result = query_with_metrics(model, prompt, temperature=temp)
        print(f"\nTemperature: {temp} (deterministic → creative)")
        print(f"Latency: {result['latency_seconds']:.2f}s")
        print(f"Response: {result['response'][:150]}...")

if __name__ == "__main__":
    test_prompt = "Write a creative story opening in one sentence:"
    
    # Compare multiple models (make sure you have them installed)
    print("Available models: llama2, mistral, neural-chat, orca, etc")
    print("Install with: ollama pull llama2")
    
    compare_models(test_prompt, models=["llama2"])
    
    # Test temperature effect
    test_temperature_effect("llama2", test_prompt)
