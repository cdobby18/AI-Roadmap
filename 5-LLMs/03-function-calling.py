"""
Function calling with local models
Let the model decide when to call Python functions
"""

import requests
import json
import re

OLLAMA_API = "http://localhost:11434/api"

# Define available functions
def get_weather(city: str) -> str:
    """Mock weather function"""
    weather_data = {
        "New York": "Sunny, 75°F",
        "London": "Cloudy, 60°F",
        "Tokyo": "Rainy, 68°F"
    }
    return weather_data.get(city, "Unknown city")

def calculate(expression: str) -> str:
    """Evaluate a math expression"""
    try:
        result = eval(expression)
        return str(result)
    except:
        return "Invalid expression"

# Function registry
FUNCTIONS = {
    "get_weather": get_weather,
    "calculate": calculate
}

def describe_functions() -> str:
    """Describe available functions for the model"""
    descriptions = """
Available functions you can call:

1. get_weather(city: str) - Get weather for a city
   Use when user asks about weather
   
2. calculate(expression: str) - Evaluate math expressions
   Use when user asks for calculations
"""
    return descriptions

def process_with_functions(model: str, user_query: str) -> str:
    """
    Send query with function descriptions and let model decide
    what to call
    """
    system_prompt = describe_functions()
    
    prompt = f"""{system_prompt}

User query: {user_query}

If you need to call a function, respond in this format:
FUNCTION: function_name(argument)

Then provide your final answer."""
    
    response = requests.post(
        f"{OLLAMA_API}/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )
    
    return response.json().get("response", "")

def execute_function_calls(response_text: str) -> str:
    """Parse response and execute any function calls"""
    # Find function calls in format: FUNCTION: function_name(arg)
    pattern = r'FUNCTION:\s*(\w+)\((.*?)\)'
    matches = re.findall(pattern, response_text)
    
    results = response_text
    for func_name, args in matches:
        if func_name in FUNCTIONS:
            # Clean up the argument string
            arg_str = args.strip().strip('"\'')
            result = FUNCTIONS[func_name](arg_str)
            results += f"\n[Function {func_name} returned: {result}]"
    
    return results

if __name__ == "__main__":
    model = "llama2"
    
    # Example: Ask for weather
    print("=== Query: Get weather for Paris ===")
    response = process_with_functions(model, "What's the weather in London?")
    print(response)
    final = execute_function_calls(response)
    print("\nAfter function execution:")
    print(final)
    
    # Example: Ask for calculation
    print("\n=== Query: Calculate 15% of 200 ===")
    response = process_with_functions(model, "Calculate 15% of 200")
    print(response)
    final = execute_function_calls(response)
    print("\nAfter function execution:")
    print(final)
