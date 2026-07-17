"""Call logging, latency tracking, and cost monitoring."""

import json
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class CallRecord:
    timestamp: str = ""
    provider: str = ""
    model: str = ""
    query: str = ""
    response: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    latency_ms: float = 0.0
    cost: float = 0.0
    error: Optional[str] = None


class Logger:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.records: list[CallRecord] = []
        self._stats = defaultdict(lambda: {"calls": 0, "total_latency": 0.0, "total_cost": 0.0, "errors": 0})

    def record(self, record: CallRecord):
        self.records.append(record)
        s = self._stats[record.provider]
        s["calls"] += 1
        s["total_latency"] += record.latency_ms
        s["total_cost"] += record.cost
        if record.error:
            s["errors"] += 1

    def summary(self) -> dict:
        return {
            provider: {
                "calls": s["calls"],
                "avg_latency_ms": round(s["total_latency"] / max(s["calls"], 1), 1),
                "total_cost": round(s["total_cost"], 6),
                "error_rate": round(s["errors"] / max(s["calls"], 1), 3),
            }
            for provider, s in self._stats.items()
        }

    def report(self) -> str:
        return json.dumps(self.summary(), indent=2)

    def log_call(
        self,
        provider: str,
        model: str,
        query: str,
        response: str,
        input_tokens: int = 0,
        output_tokens: int = 0,
        latency_ms: float = 0.0,
        cost: float = 0.0,
        error: Optional[str] = None,
    ):
        rec = CallRecord(
            timestamp=datetime.utcnow().isoformat(),
            provider=provider,
            model=model,
            query=query[:200],
            response=response[:500],
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=latency_ms,
            cost=cost,
            error=error,
        )
        self.record(rec)

        path = self.log_dir / f"calls_{datetime.utcnow().strftime('%Y%m%d')}.jsonl"
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec.__dict__) + "\n")


logger = Logger()
