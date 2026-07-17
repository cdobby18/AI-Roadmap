"""Tool registry — define, discover, and dispatch tools."""

import json
import math
import re
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class ToolSpec:
    name: str
    description: str
    parameters: dict
    fn: Callable[..., str]


_TOOL_REGISTRY: dict[str, ToolSpec] = {}


def register_tool(spec: ToolSpec):
    _TOOL_REGISTRY[spec.name] = spec


def get_tool(name: str) -> ToolSpec:
    return _TOOL_REGISTRY[name]


def get_all_tools() -> list[ToolSpec]:
    return list(_TOOL_REGISTRY.values())


def tool_schemas() -> list[dict]:
    return [
        {
            "type": "function",
            "function": {
                "name": t.name,
                "description": t.description,
                "parameters": t.parameters,
            },
        }
        for t in _TOOL_REGISTRY.values()
    ]


def dispatch(name: str, arguments: dict[str, Any]) -> str:
    tool = get_tool(name)
    return tool.fn(**arguments)


def _calculator(expression: str) -> str:
    allowed = re.sub(r"[^0-9+\-*/.() ]", "", expression)
    try:
        result = eval(allowed, {"__builtins__": {}}, {"math": math})
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def _weather(location: str) -> str:
    return f"Weather in {location}: 22°C, partly cloudy, humidity 65%."


def _web_search(query: str) -> str:
    return json.dumps(
        [
            {"title": f"Result about {query}", "snippet": f"This is a simulated search result for '{query}'."},
        ]
    )


register_tool(
    ToolSpec(
        name="calculator",
        description="Evaluate a mathematical expression",
        parameters={
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Math expression like '2 + 2' or 'sin(30)'",
                }
            },
            "required": ["expression"],
        },
        fn=_calculator,
    )
)

register_tool(
    ToolSpec(
        name="get_weather",
        description="Get current weather for a location",
        parameters={
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name"},
            },
            "required": ["location"],
        },
        fn=_weather,
    )
)

register_tool(
    ToolSpec(
        name="web_search",
        description="Search the web for information",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
            },
            "required": ["query"],
        },
        fn=_web_search,
    )
)
