"""Prompt injection detection, input validation, and rate limiting."""

import re
import time
from collections import defaultdict


INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|above)\s+instructions",
    r"forget\s+(everything|all)",
    r"you\s+are\s+(now|not\s+required)",
    r"system\s+prompt",
    r"act\s+as\s+(if\s+you\s+are|an?\s+admin)",
    r"do\s+what\s+(i|we)\s+say\s+and\s+ignore",
    r"disregard\s+",
    r"REACT\s+ACT\s+",
]


def detect_injection(text: str) -> dict:
    text_lower = text.lower()
    matches = []
    for i, pattern in enumerate(INJECTION_PATTERNS):
        if re.search(pattern, text_lower):
            matches.append({"pattern_index": i, "pattern": pattern})
    return {"injection_detected": len(matches) > 0, "matches": matches}


class RateLimiter:
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = window_seconds
        self._buckets: dict[str, list[float]] = defaultdict(list)

    def check(self, key: str = "default") -> dict:
        now = time.time()
        cutoff = now - self.window
        self._buckets[key] = [t for t in self._buckets[key] if t > cutoff]

        allowed = len(self._buckets[key]) < self.max_requests
        return {
            "allowed": allowed,
            "current_count": len(self._buckets[key]),
            "limit": self.max_requests,
            "resets_in": round(self.window - (now - (self._buckets[key][0] if self._buckets[key] else now)), 1),
        }

    def increment(self, key: str = "default"):
        self._buckets[key].append(time.time())

    def remaining(self, key: str = "default") -> int:
        now = time.time()
        cutoff = now - self.window
        self._buckets[key] = [t for t in self._buckets[key] if t > cutoff]
        return max(0, self.max_requests - len(self._buckets[key]))


rate_limiter = RateLimiter()


def validate_input(text: str) -> dict:
    issues = []
    if len(text) > 32000:
        issues.append("Input exceeds 32,000 character limit")
    if len(text) < 1:
        issues.append("Input is empty")
    injection = detect_injection(text)
    if injection["injection_detected"]:
        issues.append(f"Prompt injection patterns detected: {injection['matches']}")
    return {"valid": len(issues) == 0, "issues": issues}
