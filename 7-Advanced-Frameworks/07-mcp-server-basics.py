"""Phase 7 - MCP (Model Context Protocol) server and client.

MCP is an open protocol by Anthropic that standardises how LLMs discover and
call external tools. A server exposes tools, a client connects and routes
tool calls for the LLM.

This file covers:
1. MCP server — register tools, handle JSON-RPC requests
2. MCP client — discover tools, invoke them
3. Agent connected to MCP tools — LLM discovers and calls tools via MCP
"""

import json
import uuid
from typing import Any, Callable


# ---------------------------------------------------------------------------
# Simple JSON-RPC based MCP implementation (educational subset)
# ---------------------------------------------------------------------------

class MCPServer:
    """Minimal MCP server — hosts tools and responds to JSON-RPC requests."""

    def __init__(self, name: str = "one-piece-mcp"):
        self.name = name
        self._tools: dict[str, tuple[Callable, dict]] = {}

    def register(self, fn: Callable, name: str = "", description: str = "", parameters: dict | None = None):
        tool_name = name or fn.__name__
        self._tools[tool_name] = (
            fn,
            {
                "name": tool_name,
                "description": description or (fn.__doc__ or "").strip(),
                "parameters": parameters or self._infer_params(fn),
            },
        )

    def _infer_params(self, fn: Callable) -> dict:
        import inspect
        sig = inspect.signature(fn)
        properties = {}
        for p_name, p_param in sig.parameters.items():
            ann = p_param.annotation
            ptype = "string"
            if ann is int:
                ptype = "integer"
            elif ann is float:
                ptype = "number"
            elif ann is bool:
                ptype = "boolean"
            properties[p_name] = {"type": ptype, "description": p_name}
        return {
            "type": "object",
            "properties": properties,
            "required": list(properties.keys()),
        }

    def list_tools(self) -> list[dict]:
        return [info for _, info in self._tools.values()]

    def handle_request(self, body: dict) -> dict:
        method = body.get("method", "")
        if method == "tools/list":
            return {"jsonrpc": "2.0", "result": {"tools": self.list_tools()}, "id": body.get("id", 1)}
        elif method == "tools/call":
            params = body.get("params", {})
            tool_name = params.get("name", "")
            args = params.get("arguments", {})
            fn, _ = self._tools.get(tool_name, (None, None))
            if not fn:
                return {"jsonrpc": "2.0", "error": {"code": -32601, "message": f"Tool not found: {tool_name}"}, "id": body.get("id", 1)}
            try:
                result = fn(**args)
                return {"jsonrpc": "2.0", "result": {"content": [{"type": "text", "text": str(result)}]}, "id": body.get("id", 1)}
            except Exception as e:
                return {"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}, "id": body.get("id", 1)}
        else:
            return {"jsonrpc": "2.0", "error": {"code": -32601, "message": f"Unknown method: {method}"}, "id": body.get("id", 1)}


class MCPClient:
    """Minimal MCP client — connects to a server and exposes tools to an agent."""

    def __init__(self, server: MCPServer):
        self.server = server

    def list_tools(self) -> list[dict]:
        resp = self.server.handle_request({"jsonrpc": "2.0", "method": "tools/list", "id": 1})
        return resp.get("result", {}).get("tools", [])

    def call_tool(self, name: str, args: dict) -> str:
        resp = self.server.handle_request({
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": name, "arguments": args},
            "id": str(uuid.uuid4()),
        })
        if "error" in resp:
            raise RuntimeError(resp["error"]["message"])
        contents = resp.get("result", {}).get("content", [])
        return "\n".join(c["text"] for c in contents if c["type"] == "text")


# ---------------------------------------------------------------------------
# 1. Build an MCP server with One Piece tools
# ---------------------------------------------------------------------------

def demo_mcp_server():
    server = MCPServer(name="one-piece-mcp")

    def get_crew(member: str) -> str:
        """Get information about a Straw Hat crew member."""
        crew = {
            "luffy": "Monkey D. Luffy — captain, Gomu Gomu no Mi, wants to be Pirate King",
            "zoro": "Roronoa Zoro — swordsman, three swords, world's greatest goal",
            "nami": "Nami — navigator, weather sense, wants to map the world",
            "sanji": "Sanji — chef, Black Leg style, seeks the All Blue",
            "robin": "Nico Robin — archaeologist, Hana Hana no Mi, seeks true history",
        }
        return crew.get(member.lower(), f"No data on '{member}'")

    def get_devil_fruit(name: str) -> str:
        """Get information about a Devil Fruit."""
        fruits = {
            "gomu gomu no mi": "Paramecia — grants rubber properties. Eaten by Luffy.",
            "hana hana no mi": "Paramecia — sprout body parts anywhere. Eaten by Robin.",
            "yami yami no mi": "Logia — darkness control. Eaten by Blackbeard.",
            "mera mera no mi": "Logia — fire control. Eaten by Ace then Sabo.",
        }
        return fruits.get(name.lower(), f"No data on '{name}'")

    server.register(get_crew)
    server.register(get_devil_fruit)

    print(f"1. MCP Server '{server.name}' online")
    tools = server.list_tools()
    print(f"   Registered {len(tools)} tools:")
    for t in tools:
        print(f"   - {t['name']}: {t['description']}")

    client = MCPClient(server)
    print(f"\n   Client connected. {len(client.list_tools())} tools discovered.")
    print()

    print("   Calling tools via MCP:")
    result = client.call_tool("get_crew", {"member": "zoro"})
    print(f"   get_crew('zoro') -> {result}")
    result = client.call_tool("get_devil_fruit", {"name": "mera mera no mi"})
    print(f"   get_devil_fruit('mera...') -> {result}")
    print()


# ---------------------------------------------------------------------------
# 2. Agent using MCP tools — LangChain agent discovers MCP-hosted tools
# ---------------------------------------------------------------------------

def demo_mcp_agent():
    from langchain_core.tools import tool
    from langchain.agents import create_agent
    from langchain_ollama import ChatOllama
    from langchain_core.messages import HumanMessage

    server = MCPServer(name="mcp-agent-server")

    def search_island(name: str) -> str:
        """Get information about an island in One Piece."""
        islands = {
            "drum": "Winter island. Former kingdom of the Sakura. Home of Kureha and Chopper.",
            "water 7": "City of shipwrights. Home of Galley-La Company and Franky.",
            "skypiea": "Sky island above the White-White Sea. Home of the Shandians.",
            "enies lobby": "Government judicial island. Site of the Buster Call.",
            "sabaody": "Archipelago of mangrove trees. Gateway to Fish-Man Island.",
        }
        return islands.get(name.lower(), f"No data on '{name}'")

    def estimate_bounty(name: str) -> str:
        """Get the current bounty of a Straw Hat crew member."""
        bounties = {
            "luffy": "3,000,000,000 (Yonko)",
            "zoro": "1,111,000,000",
            "sanji": "1,032,000,000",
            "jinbe": "1,100,000,000",
            "robin": "930,000,000",
            "usopp": "500,000,000 (God Usopp)",
        }
        return bounties.get(name.lower(), "Unknown")

    server.register(search_island)
    server.register(estimate_bounty)
    client = MCPClient(server)

    @tool
    def mcp_search_island(name: str) -> str:
        """Search for information about an island in One Piece world."""
        return client.call_tool("search_island", {"name": name})

    @tool
    def mcp_estimate_bounty(name: str) -> str:
        """Get the bounty of a Straw Hat crew member."""
        return client.call_tool("estimate_bounty", {"name": name})

    llm = ChatOllama(model="llama2", temperature=0.0)
    agent = create_agent(model=llm, tools=[mcp_search_island, mcp_estimate_bounty])

    print("2. MCP Agent — questions answered via MCP-hosted tools:")
    questions = [
        "What island is known as the winter kingdom?",
        "What is Sanji's bounty?",
    ]
    for q in questions:
        result = agent.invoke({"messages": [("human", q)]})
        answer = result["messages"][-1].content
        print(f"   Q: {q}")
        print(f"   A: {answer}")
        print()
    print()


# ---------------------------------------------------------------------------
# 3. MCP lifecycle — connect / list / call / disconnect
# ---------------------------------------------------------------------------

def demo_lifecycle():
    print("3. MCP lifecycle (conceptual):")
    print("""
   MCP servers follow this lifecycle:

    CLIENT                      SERVER
      |                           |
      |-- initialize ------------>|
      |<-- server_info -----------|
      |                           |
      |-- tools/list ------------>|
      |<-- tool_list -------------|
      |                           |
      |-- tools/call {name,args}>|
      |<-- tool_result -----------|
      |                           |
      |-- shutdown --------------->|
      |<-- closed -----------------|

   The MCP protocol uses JSON-RPC 2.0 over stdio or HTTP transport.
   In production, use the official 'mcp' Python package:

     from mcp.server.fastmcp import FastMCP
     server = FastMCP("my-server")
     @server.tool()
     def my_tool(param: str) -> str:
         return f"Result: {param}"
     server.run()

   The LangChain MCP adapter (langchain-mcp-adapters) lets agents
   connect to MCP servers automatically:

     from langchain_mcp_adapters.client import MultiServerMCPClient
     async with MultiServerMCPClient() as client:
         tools = client.get_tools()
         agent = create_agent(model=llm, tools=tools)
   """)
    print()


# ---------------------------------------------------------------------------
# Safe runner
# ---------------------------------------------------------------------------

def try_demo(fn, name: str):
    try:
        fn()
    except Exception as e:
        msg = str(e)
        if "Connection refused" in msg or "WinError 10061" in msg or "actively refused" in msg:
            print(f"[SKIP] {name} — Ollama not running. Start with: ollama serve\n")
        else:
            import traceback
            print(f"[ERROR] {name}: {msg}")
            traceback.print_exc()
            print()


if __name__ == "__main__":
    print("=" * 60)
    print("MCP Server & Client — Tool Hosting, Discovery, Agent Integration")
    print("=" * 60)
    demo_mcp_server()
    try_demo(demo_mcp_agent, "MCP Agent")
    demo_lifecycle()
