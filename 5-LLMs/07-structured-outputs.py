"""
Structured Outputs with LLMs
Force models to return valid JSON with proper schema validation
"""

import json
import requests
from typing import Any

OLLAMA_API = "http://localhost:11434/api"

def structured_output_ollama(model: str, prompt: str, schema: dict) -> dict:
    """
    Request structured JSON output from Ollama
    Include schema in prompt to guide model
    """
    
    schema_str = json.dumps(schema, indent=2)
    
    structured_prompt = f"""{prompt}

Please respond ONLY with valid JSON matching this schema:
{schema_str}

Do not include any text before or after the JSON."""
    
    response = requests.post(
        f"{OLLAMA_API}/generate",
        json={
            "model": model,
            "prompt": structured_prompt,
            "stream": False
        },
        timeout=120
    )
    
    text = response.json().get("response", "").strip()
    
    # Extract JSON from response
    try:
        # Try to find JSON object in response
        start = text.find('{')
        end = text.rfind('}') + 1
        
        if start >= 0 and end > start:
            json_str = text[start:end]
            return json.loads(json_str)
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON response: {e}", "raw": text}
    
    return {"error": "No JSON found in response", "raw": text}

def extract_information_structured(model: str, text: str) -> dict:
    """
    Extract structured info from unstructured text
    """
    
    schema = {
        "type": "object",
        "properties": {
            "entities": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "type": {"type": "string"},
                        "description": {"type": "string"}
                    }
                }
            },
            "sentiment": {"type": "string", "enum": ["positive", "negative", "neutral"]},
            "summary": {"type": "string"},
            "confidence": {"type": "number", "minimum": 0, "maximum": 1}
        },
        "required": ["entities", "sentiment", "summary", "confidence"]
    }
    
    prompt = f"""Extract structured information from this text:

"{text}"

Return JSON with:
- entities: List of named entities (people, places, things)
- sentiment: Overall sentiment
- summary: One sentence summary
- confidence: Your confidence (0-1)"""
    
    return structured_output_ollama(model, prompt, schema)

def generate_product_catalog(model: str, category: str) -> list:
    """
    Generate structured product data
    """
    
    item_schema = {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "price": {"type": "number"},
            "description": {"type": "string"},
            "tags": {"type": "array", "items": {"type": "string"}},
            "in_stock": {"type": "boolean"}
        },
        "required": ["id", "name", "price", "description"]
    }
    
    schema = {
        "type": "object",
        "properties": {
            "products": {
                "type": "array",
                "items": item_schema
            }
        }
    }
    
    prompt = f"""Generate 3 realistic products for the {category} category.
    
Return a JSON object with a 'products' array."""
    
    result = structured_output_ollama(model, prompt, schema)
    
    return result.get("products", []) if "products" in result else []

if __name__ == "__main__":
    # Get available models
    response = requests.get(f"{OLLAMA_API}/tags")
    models = [m["name"] for m in response.json().get("models", [])]
    
    if not models:
        print("No models available. Run: ollama pull llama2")
        exit(1)
    
    model = models[0]
    print(f"Using model: {model}\n")
    
    # Test 1: Extract structured info
    print("=" * 60)
    print("TEST 1: Extract Information")
    print("=" * 60)
    
    text = "John Smith from New York works at Microsoft. He loves Python and machine learning."
    print(f"Input: {text}\n")
    
    result = extract_information_structured(model, text)
    print("Extracted:")
    print(json.dumps(result, indent=2))
    
    # Test 2: Generate product catalog
    print("\n" + "=" * 60)
    print("TEST 2: Generate Product Catalog")
    print("=" * 60)
    
    products = generate_product_catalog(model, "electronics")
    print("Generated products:")
    print(json.dumps(products, indent=2))
