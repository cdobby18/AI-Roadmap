"""
LLM Observability & Monitoring
Track performance, costs, tokens, and errors with LangSmith patterns
"""

import json
import time
import requests
from datetime import datetime
from typing import Dict, List, Any
from collections import defaultdict

OLLAMA_API = "http://localhost:11434/api"

class LLMObserver:
    """Track LLM calls and performance metrics"""
    
    def __init__(self):
        self.calls = []
        self.metrics = defaultdict(list)
    
    def log_call(self, model: str, prompt: str, response: str, latency: float, 
                 tokens_in: int, tokens_out: int, cost: float = 0.0, error: str = None):
        """Log an LLM call"""
        
        call_record = {
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "prompt_length": len(prompt),
            "response_length": len(response),
            "latency_seconds": latency,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "cost": cost,
            "error": error
        }
        
        self.calls.append(call_record)
        
        # Track metrics
        self.metrics["latency"].append(latency)
        self.metrics["tokens_in"].append(tokens_in)
        self.metrics["tokens_out"].append(tokens_out)
        self.metrics["cost"].append(cost)
        
        if error:
            self.metrics["errors"].append(error)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get aggregated statistics"""
        
        if not self.calls:
            return {"error": "No calls recorded"}
        
        latencies = self.metrics["latency"]
        tokens_in = self.metrics["tokens_in"]
        tokens_out = self.metrics["tokens_out"]
        costs = self.metrics["cost"]
        errors = self.metrics["errors"]
        
        return {
            "total_calls": len(self.calls),
            "errors": len(errors),
            "latency": {
                "min": min(latencies),
                "max": max(latencies),
                "avg": sum(latencies) / len(latencies),
                "p95": sorted(latencies)[int(len(latencies) * 0.95)]
            },
            "tokens": {
                "total_in": sum(tokens_in),
                "total_out": sum(tokens_out),
                "avg_in": sum(tokens_in) / len(tokens_in),
                "avg_out": sum(tokens_out) / len(tokens_out)
            },
            "cost": {
                "total": sum(costs),
                "avg_per_call": sum(costs) / len(costs) if costs else 0
            }
        }
    
    def print_report(self):
        """Print human-readable report"""
        
        stats = self.get_stats()
        
        if "error" in stats:
            print(stats["error"])
            return
        
        print("=" * 60)
        print("LLM CALL STATISTICS")
        print("=" * 60)
        print(f"\nTotal Calls: {stats['total_calls']}")
        print(f"Errors: {stats['errors']}")
        
        print(f"\nLatency (seconds):")
        print(f"  Min: {stats['latency']['min']:.2f}s")
        print(f"  Avg: {stats['latency']['avg']:.2f}s")
        print(f"  Max: {stats['latency']['max']:.2f}s")
        print(f"  P95: {stats['latency']['p95']:.2f}s")
        
        print(f"\nTokens:")
        print(f"  Input: {stats['tokens']['total_in']} (avg: {stats['tokens']['avg_in']:.0f})")
        print(f"  Output: {stats['tokens']['total_out']} (avg: {stats['tokens']['avg_out']:.0f})")
        print(f"  Total: {stats['tokens']['total_in'] + stats['tokens']['total_out']}")
        
        if stats['cost']['total'] > 0:
            print(f"\nCost:")
            print(f"  Total: ${stats['cost']['total']:.4f}")
            print(f"  Per call: ${stats['cost']['avg_per_call']:.6f}")
    
    def to_json(self) -> str:
        """Export logs as JSON"""
        return json.dumps(self.calls, indent=2)

class LLMTrace:
    """Trace a single LLM call with detailed metrics"""
    
    def __init__(self, name: str, model: str):
        self.name = name
        self.model = model
        self.start_time = None
        self.end_time = None
        self.metadata = {}
    
    def start(self):
        """Start tracing"""
        self.start_time = time.time()
    
    def end(self):
        """End tracing"""
        self.end_time = time.time()
    
    def get_duration(self) -> float:
        """Get duration in seconds"""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0
    
    def set_metadata(self, key: str, value: Any):
        """Add metadata"""
        self.metadata[key] = value
    
    def get_summary(self) -> Dict[str, Any]:
        """Get trace summary"""
        return {
            "name": self.name,
            "model": self.model,
            "duration": self.get_duration(),
            "metadata": self.metadata
        }

class TokenCounter:
    """Estimate token usage (model-specific)"""
    
    # Rough token ratios (tokens per character)
    CHAR_TO_TOKEN = {
        "llama2": 1/4,
        "gpt-3.5-turbo": 1/4,
        "gpt-4": 1/3,
        "claude": 1/4,
        "gemini": 1/3,
    }
    
    @staticmethod
    def count(text: str, model: str = "llama2") -> int:
        """Estimate token count"""
        ratio = TokenCounter.CHAR_TO_TOKEN.get(model, 1/4)
        return int(len(text) * ratio)

class CostCalculator:
    """Calculate API costs"""
    
    # Approximate costs (USD)
    PRICING = {
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},  # per 1K tokens
        "gpt-4": {"input": 0.03, "output": 0.06},
        "claude-3": {"input": 0.003, "output": 0.015},
        "gemini-pro": {"input": 0.0005, "output": 0.0015},
        "ollama": {"input": 0, "output": 0},  # Free
    }
    
    @staticmethod
    def calculate(model: str, tokens_in: int, tokens_out: int) -> float:
        """Calculate cost for API call"""
        
        pricing = CostCalculator.PRICING.get(model, {"input": 0, "output": 0})
        
        cost_in = (tokens_in / 1000) * pricing["input"]
        cost_out = (tokens_out / 1000) * pricing["output"]
        
        return cost_in + cost_out

def demo_observability():
    """Demonstrate observability features"""
    
    # Setup
    observer = LLMObserver()
    
    response = requests.get(f"{OLLAMA_API}/tags")
    models = [m["name"] for m in response.json().get("models", [])]
    
    if not models:
        print("No models. Run: ollama pull llama2")
        return
    
    model = models[0]
    print(f"Using model: {model}\n")
    
    # Simulate LLM calls with tracing
    test_prompts = [
        "What is Python?",
        "Explain machine learning in simple terms",
        "Write a function to calculate Fibonacci numbers"
    ]
    
    for prompt in test_prompts:
        # Create trace
        trace = LLMTrace(f"Call: {prompt[:30]}", model)
        trace.start()
        
        try:
            # Make LLM call
            response = requests.post(
                f"{OLLAMA_API}/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120
            )
            
            response_text = response.json().get("response", "")
            
        except Exception as e:
            response_text = ""
            trace.set_metadata("error", str(e))
        
        trace.end()
        
        # Calculate metrics
        tokens_in = TokenCounter.count(prompt, model)
        tokens_out = TokenCounter.count(response_text, model)
        cost = CostCalculator.calculate(model, tokens_in, tokens_out)
        
        # Log call
        observer.log_call(
            model=model,
            prompt=prompt,
            response=response_text,
            latency=trace.get_duration(),
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            cost=cost
        )
        
        trace.set_metadata("tokens_in", tokens_in)
        trace.set_metadata("tokens_out", tokens_out)
        trace.set_metadata("cost", cost)
        
        print(f"✓ {trace.name}")
        print(f"  Duration: {trace.get_duration():.2f}s")
        print(f"  Tokens: {tokens_in} → {tokens_out}")
        print(f"  Cost: ${cost:.6f}\n")
    
    # Print report
    observer.print_report()
    
    # Export logs
    print("\nLogs (JSON):")
    print(observer.to_json()[:500] + "...")

if __name__ == "__main__":
    demo_observability()
