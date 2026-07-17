"""Unified interface over multiple LLM providers."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional

import requests

from config import settings


@dataclass
class LLMResponse:
    content: str
    model: str
    provider: str
    input_tokens: int = 0
    output_tokens: int = 0
    latency_ms: float = 0.0
    cost: float = 0.0


class BaseProvider(ABC):
    @abstractmethod
    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> LLMResponse:
        ...

    @abstractmethod
    def generate_structured(
        self,
        prompt: str,
        json_schema: dict,
        system: Optional[str] = None,
        temperature: float = 0.0,
    ) -> LLMResponse:
        ...


class OpenAIProvider(BaseProvider):
    def __init__(self):
        import openai as _openai

        self.client = _openai.OpenAI(api_key=settings.openai.api_key)
        self.model = settings.openai.default_model
        self.cfg = settings.openai

    def generate(self, prompt, system=None, temperature=0.7, max_tokens=1024):
        import time

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        start = time.time()
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        elapsed = (time.time() - start) * 1000
        choice = resp.choices[0]
        usage = resp.usage or type("u", (), {"prompt_tokens": 0, "completion_tokens": 0})
        cost = (usage.prompt_tokens / 1000 * self.cfg.cost_per_1k_input) + (
            usage.completion_tokens / 1000 * self.cfg.cost_per_1k_output
        )
        return LLMResponse(
            content=choice.message.content,
            model=self.model,
            provider="openai",
            input_tokens=usage.prompt_tokens,
            output_tokens=usage.completion_tokens,
            latency_ms=round(elapsed, 1),
            cost=round(cost, 6),
        )

    def generate_structured(self, prompt, json_schema, system=None, temperature=0.0):
        import json, time

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        start = time.time()
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            response_format={"type": "json_object"},
        )
        elapsed = (time.time() - start) * 1000
        choice = resp.choices[0]
        usage = resp.usage or type("u", (), {"prompt_tokens": 0, "completion_tokens": 0})

        try:
            json.loads(choice.message.content)
        except json.JSONDecodeError:
            pass

        cost = (usage.prompt_tokens / 1000 * self.cfg.cost_per_1k_input) + (
            usage.completion_tokens / 1000 * self.cfg.cost_per_1k_output
        )
        return LLMResponse(
            content=choice.message.content,
            model=self.model,
            provider="openai",
            input_tokens=usage.prompt_tokens,
            output_tokens=usage.completion_tokens,
            latency_ms=round(elapsed, 1),
            cost=round(cost, 6),
        )


class OllamaProvider(BaseProvider):
    def __init__(self):
        self.base_url = settings.ollama.base_url.rstrip("/")
        self.model = settings.ollama.default_model

    def _call(self, payload: dict) -> dict:
        import time

        start = time.time()
        resp = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=120)
        resp.raise_for_status()
        elapsed = (time.time() - start) * 1000
        data = resp.json()
        data["_latency_ms"] = round(elapsed, 1)
        return data

    def generate(self, prompt, system=None, temperature=0.7, max_tokens=1024):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system or "",
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }
        data = self._call(payload)
        return LLMResponse(
            content=data.get("response", ""),
            model=self.model,
            provider="ollama",
            input_tokens=data.get("prompt_eval_count", 0),
            output_tokens=data.get("eval_count", 0),
            latency_ms=data.get("_latency_ms", 0),
            cost=0.0,
        )

    def generate_structured(self, prompt, json_schema, system=None, temperature=0.0):
        import json

        schema_instruction = f'\nRespond with valid JSON matching this schema: {json.dumps(json_schema)}'
        return self.generate(prompt + schema_instruction, system=system, temperature=temperature)


class AnthropicProvider(BaseProvider):
    def __init__(self):
        import anthropic as _anthropic

        self.client = _anthropic.Anthropic(api_key=settings.anthropic.api_key)
        self.model = settings.anthropic.default_model
        self.cfg = settings.anthropic

    def generate(self, prompt, system=None, temperature=0.7, max_tokens=1024):
        import time

        start = time.time()
        resp = self.client.messages.create(
            model=self.model,
            system=system or "",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        elapsed = (time.time() - start) * 1000
        usage = resp.usage
        cost = (usage.input_tokens / 1000 * self.cfg.cost_per_1k_input) + (
            usage.output_tokens / 1000 * self.cfg.cost_per_1k_output
        )
        return LLMResponse(
            content=resp.content[0].text,
            model=self.model,
            provider="anthropic",
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
            latency_ms=round(elapsed, 1),
            cost=round(cost, 6),
        )

    def generate_structured(self, prompt, json_schema, system=None, temperature=0.0):
        import json

        schema_instruction = f'\nRespond with valid JSON matching this schema: {json.dumps(json_schema)}'
        return self.generate(prompt + schema_instruction, system=system, temperature=temperature)


_PROVIDER_CACHE: dict[str, BaseProvider] = {}


def get_provider(name: str) -> BaseProvider:
    if name not in _PROVIDER_CACHE:
        match name:
            case "openai":
                _PROVIDER_CACHE[name] = OpenAIProvider()
            case "anthropic":
                _PROVIDER_CACHE[name] = AnthropicProvider()
            case "ollama":
                _PROVIDER_CACHE[name] = OllamaProvider()
            case _:
                raise ValueError(f"Unknown provider: {name}")
    return _PROVIDER_CACHE[name]
