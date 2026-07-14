"""
Tool Calling with LLMs
Advanced function calling with schemas and proper tool definitions
Similar to OpenAI's function calling API
"""

import json
import requests
from typing import Callable, Any
from datetime import datetime

OLLAMA_API = "http://localhost:11434/api"

class Tool:
    """Define a tool the LLM can call"""
    
    def __init__(self, name: str, description: str, func: Callable, parameters: dict):
        self.name = name
        self.description = description
        self.func = func
        self.parameters = parameters
    
    def to_dict(self):
        """Convert to tool schema"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }

class ToolKit:
    """Manage a set of tools"""
    
    def __init__(self):
        self.tools = {}
        self._setup_default_tools()
    
    def _setup_default_tools(self):
        """Setup common tools"""
        
        # Weather tool
        self.add_tool(
            name="get_weather",
            description="Get current weather for a city",
            func=self._mock_weather,
            parameters={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit"
                    }
                },
                "required": ["city"]
            }
        )
        
        # Calculator tool
        self.add_tool(
            name="calculate",
            description="Perform mathematical calculations",
            func=self._calculate,
            parameters={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Math expression to evaluate"
                    }
                },
                "required": ["expression"]
            }
        )
        
        # Search tool
        self.add_tool(
            name="search_knowledge_base",
            description="Search internal knowledge base for information",
            func=self._search_kb,
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "category": {
                        "type": "string",
                        "enum": ["docs", "faq", "code_examples"],
                        "description": "Search category"
                    }
                },
                "required": ["query"]
            }
        )
    
    def add_tool(self, name: str, description: str, func: Callable, parameters: dict):
        """Add a tool to the kit"""
        self.tools[name] = Tool(name, description, func, parameters)
    
    def get_tools_schema(self):
        """Get schema for all tools"""
        return [tool.to_dict() for tool in self.tools.values()]
    
    def call_tool(self, name: str, **kwargs) -> Any:
        """Execute a tool"""
        if name not in self.tools:
            return {"error": f"Tool '{name}' not found"}
        
        try:
            return self.tools[name].func(**kwargs)
        except Exception as e:
            return {"error": str(e)}
    
    # Mock implementations
    def _mock_weather(self, city: str, unit: str = "celsius") -> dict:
        weather_data = {
            "New York": {"temp": 22, "condition": "Sunny"},
            "London": {"temp": 18, "condition": "Cloudy"},
            "Tokyo": {"temp": 25, "condition": "Rainy"},
            "Paris": {"temp": 20, "condition": "Partly Cloudy"}
        }
        
        data = weather_data.get(city, {"temp": 20, "condition": "Unknown"})
        
        if unit == "fahrenheit":
            data["temp"] = data["temp"] * 9/5 + 32
            data["unit"] = "°F"
        else:
            data["unit"] = "°C"
        
        return data
    
    def _calculate(self, expression: str) -> dict:
        try:
            result = eval(expression)
            return {"result": result, "expression": expression}
        except Exception as e:
            return {"error": str(e)}
    
    def _search_kb(self, query: str, category: str = "docs") -> dict:
        kb = {
            "docs": {
                "python": "Python is a high-level programming language",
                "fastapi": "FastAPI is a modern Python web framework",
                "llm": "LLM stands for Large Language Model"
            },
            "faq": {
                "how to install": "Use pip install package_name",
                "what is": "A concept or technology"
            },
            "code_examples": {
                "hello world": "print('Hello World')",
                "loop": "for i in range(10): print(i)"
            }
        }
        
        results = []
        search_dict = kb.get(category, {})
        
        for key, value in search_dict.items():
            if query.lower() in key.lower() or query.lower() in value.lower():
                results.append({"key": key, "value": value})
        
        return {"results": results, "count": len(results)}

def use_tools_with_llm(model: str, user_query: str, toolkit: ToolKit) -> str:
    """
    Multi-turn interaction where LLM uses tools
    """
    
    tools_schema = toolkit.get_tools_schema()
    
    system_prompt = f"""You are a helpful assistant with access to tools.
    
When you need information, use the available tools.
Respond naturally and use tool results to answer the user.

Available tools:
{json.dumps([t['function'] for t in tools_schema], indent=2)}"""
    
    # First request to model
    messages = [
        {"role": "user", "content": user_query}
    ]
    
    response = requests.post(
        f"{OLLAMA_API}/chat",
        json={
            "model": model,
            "messages": messages,
            "system": system_prompt,
            "stream": False
        },
        timeout=120
    )
    
    assistant_response = response.json()["message"]["content"]
    
    # Simple tool detection in response
    # In production, use proper function calling support
    tool_calls = _extract_tool_calls(assistant_response)
    
    if tool_calls:
        for tool_name, tool_args in tool_calls:
            tool_result = toolkit.call_tool(tool_name, **tool_args)
            
            # Get final response with tool results
            messages.append({"role": "assistant", "content": assistant_response})
            messages.append({
                "role": "user",
                "content": f"Tool {tool_name} returned: {json.dumps(tool_result)}"
            })
            
            response = requests.post(
                f"{OLLAMA_API}/chat",
                json={
                    "model": model,
                    "messages": messages,
                    "stream": False
                },
                timeout=120
            )
            
            assistant_response = response.json()["message"]["content"]
    
    return assistant_response

def _extract_tool_calls(text: str) -> list:
    """Extract tool calls from model response"""
    import re
    
    # Look for patterns like: TOOL: tool_name(arg1=value1, arg2=value2)
    pattern = r'TOOL:\s*(\w+)\((.*?)\)'
    matches = re.findall(pattern, text)
    
    tool_calls = []
    for tool_name, args_str in matches:
        try:
            # Parse arguments (simplified)
            args_dict = {}
            for arg in args_str.split(','):
                if '=' in arg:
                    k, v = arg.split('=', 1)
                    args_dict[k.strip()] = v.strip().strip('"\'')
            tool_calls.append((tool_name, args_dict))
        except:
            pass
    
    return tool_calls

if __name__ == "__main__":
    # Get available models
    response = requests.get(f"{OLLAMA_API}/tags")
    models = [m["name"] for m in response.json().get("models", [])]
    
    if not models:
        print("No models. Run: ollama pull llama2")
        exit(1)
    
    model = models[0]
    print(f"Using model: {model}\n")
    
    # Create toolkit
    toolkit = ToolKit()
    
    print("Available tools:")
    for tool in toolkit.tools.values():
        print(f"  - {tool.name}: {tool.description}")
    
    # Test queries
    queries = [
        "What's the weather in London?",
        "Calculate 25 * 4",
        "Search for information about Python"
    ]
    
    for query in queries:
        print(f"\n{'=' * 60}")
        print(f"Query: {query}")
        print(f"{'=' * 60}")
        
        result = use_tools_with_llm(model, query, toolkit)
        print(f"Response: {result}")
