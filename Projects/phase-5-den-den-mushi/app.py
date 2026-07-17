"""Den Den Mushi — CLI + FastAPI entry point."""

import argparse
import json
import sys

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from providers import get_provider
from router import route
from tools import dispatch, tool_schemas
from memory import Conversation
from structured_output import SENTIMENT_SCHEMA, EXTRACTION_SCHEMA, parse_structured, SentimentResult, ExtractionResult
from security import validate_input, rate_limiter
from observability import logger
from evaluate import run_benchmark

fastapi_app = FastAPI(title="Den Den Mushi", version="1.0.0")


class AskRequest(BaseModel):
    query: str
    provider: str = "auto"
    temperature: float = 0.7
    use_tools: bool = False


class AskResponse(BaseModel):
    query: str
    provider: str
    response: str
    latency_ms: float
    cost: float


class ChatRequest(BaseModel):
    query: str
    provider: str = "ollama"


def handle_query(query: str, provider: str = "auto", temperature: float = 0.7, use_tools: bool = False) -> dict:
    validation = validate_input(query)
    if not validation["valid"]:
        return {"error": "; ".join(validation["issues"])}

    rate_check = rate_limiter.check()
    if not rate_check["allowed"]:
        return {"error": f"Rate limit exceeded. Resets in {rate_check['resets_in']}s"}

    rate_limiter.increment()

    if use_tools:
        system = "You have access to tools. When a user asks a question that requires computation or lookup, respond with a JSON tool call."
        provider_name, llm_resp = route(query, preferred_provider="openai" if provider == "auto" else provider, system=system)
        import re
        tool_match = re.search(r'"tool"\s*:\s*"(\w+)"', llm_resp.content)
        if tool_match:
            tool_name = tool_match.group(1)
            args = {"expression": query} if tool_name == "calculator" else {"query": query}
            tool_result = dispatch(tool_name, args)
            provider_name, llm_resp = route(
                f"Question: {query}\nTool result: {tool_result}\nAnswer the question using the tool result.",
                preferred_provider=provider_name,
            )
    else:
        provider_name, llm_resp = route(query, preferred_provider=provider, temperature=temperature)

    logger.log_call(
        provider=provider_name,
        model=llm_resp.model,
        query=query,
        response=llm_resp.content,
        input_tokens=llm_resp.input_tokens,
        output_tokens=llm_resp.output_tokens,
        latency_ms=llm_resp.latency_ms,
        cost=llm_resp.cost,
    )

    return {
        "query": query,
        "provider": provider_name,
        "model": llm_resp.model,
        "response": llm_resp.content,
        "latency_ms": llm_resp.latency_ms,
        "cost": llm_resp.cost,
        "input_tokens": llm_resp.input_tokens,
        "output_tokens": llm_resp.output_tokens,
    }


@fastapi_app.post("/ask", response_model=AskResponse)
def ask_endpoint(req: AskRequest):
    result = handle_query(req.query, req.provider, req.temperature, req.use_tools)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return AskResponse(
        query=result["query"],
        provider=result["provider"],
        response=result["response"],
        latency_ms=result["latency_ms"],
        cost=result["cost"],
    )


@fastapi_app.get("/health")
def health():
    return {"status": "ok", "providers": ["openai", "anthropic", "ollama"]}


@fastapi_app.get("/metrics")
def metrics():
    return logger.summary()


@fastapi_app.get("/tools")
def list_tools():
    return {"tools": tool_schemas()}


def cli():
    parser = argparse.ArgumentParser(description="Den Den Mushi — LLM Communications Hub")
    sub = parser.add_subparsers(dest="command")

    ask_p = sub.add_parser("ask", help="Ask a single question")
    ask_p.add_argument("query", nargs="*", help="Your question")
    ask_p.add_argument("--provider", default="auto")
    ask_p.add_argument("--tool-use", action="store_true")
    ask_p.add_argument("--temperature", type=float, default=0.7)

    sub.add_parser("chat", help="Interactive chat mode")
    sub.add_parser("benchmark", help="Run evaluation benchmark")
    sub.add_parser("metrics", help="Show observability summary")

    args = parser.parse_args()

    match args.command:
        case "ask":
            query = " ".join(args.query) if args.query else input("Query: ")
            result = handle_query(query, args.provider, args.temperature, args.tool_use)
            print(json.dumps(result, indent=2))

        case "chat":
            conv = Conversation(system="You are a helpful assistant.")
            print("Den Den Mushi chat. Type /exit to quit.\n")
            while True:
                query = input("You: ")
                if query.strip().lower() in ("/exit", "/quit"):
                    break
                conv.add("user", query)
                result = handle_query(conv.build_prompt())
                print(f"Bot ({result['provider']}): {result['response']}\n")
                conv.add("assistant", result["response"])

        case "benchmark":
            result = run_benchmark()
            print(json.dumps(result, indent=2))

        case "metrics":
            print(logger.report())

        case _:
            parser.print_help()


if __name__ == "__main__":
    cli()
