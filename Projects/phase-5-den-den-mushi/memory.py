"""Conversation memory with token budgeting."""

from dataclasses import dataclass, field


@dataclass
class Turn:
    role: str
    content: str
    tokens: int = 0


@dataclass
class Conversation:
    system: str = ""
    turns: list[Turn] = field(default_factory=list)
    max_tokens: int = 4096
    _approx_tokens: int = 0

    def add(self, role: str, content: str):
        tokens = len(content) // 4
        self.turns.append(Turn(role=role, content=content, tokens=tokens))
        self._approx_tokens += tokens
        self._trim()

    def _trim(self):
        budget = self.max_tokens - (len(self.system) // 4)
        while self._approx_tokens > budget and len(self.turns) > 2:
            removed = self.turns.pop(0)
            self._approx_tokens -= removed.tokens

    def build_prompt(self) -> str:
        lines = [f"System: {self.system}"] if self.system else []
        for t in self.turns:
            prefix = "User" if t.role == "user" else "Assistant"
            lines.append(f"{prefix}: {t.content}")
        return "\n".join(lines)

    def token_usage(self) -> dict:
        return {
            "total_tokens": self._approx_tokens,
            "turn_count": len(self.turns),
            "budget_remaining": self.max_tokens - self._approx_tokens,
        }


def estimate_tokens(text: str) -> int:
    return len(text) // 4
