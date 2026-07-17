"""Provider configuration from environment variables."""

import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ProviderConfig:
    name: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    default_model: str = ""
    max_tokens: int = 4096
    cost_per_1k_input: float = 0.0
    cost_per_1k_output: float = 0.0


@dataclass
class Settings:
    openai: ProviderConfig = field(
        default_factory=lambda: ProviderConfig(
            name="openai",
            api_key=os.getenv("OPENAI_API_KEY"),
            default_model="gpt-4o-mini",
            cost_per_1k_input=0.00015,
            cost_per_1k_output=0.0006,
        )
    )
    anthropic: ProviderConfig = field(
        default_factory=lambda: ProviderConfig(
            name="anthropic",
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            default_model="claude-3-haiku-20240307",
            cost_per_1k_input=0.00025,
            cost_per_1k_output=0.00125,
        )
    )
    ollama: ProviderConfig = field(
        default_factory=lambda: ProviderConfig(
            name="ollama",
            base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
            default_model=os.getenv("OLLAMA_MODEL", "llama2"),
            cost_per_1k_input=0.0,
            cost_per_1k_output=0.0,
        )
    )
    rate_limit_rpm: int = int(os.getenv("RATE_LIMIT_RPM", "60"))
    rate_limit_period_seconds: int = 60


settings = Settings()
