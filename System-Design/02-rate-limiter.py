"""
Token-Bucket Rate Limiter — guided exercise.

Theory: Notes/system-design-patterns.md -> "rate limiting / throttling".

The mental model: every client has a bucket that holds up to `capacity`
tokens. Tokens drip in at `refill_rate` per second. Each request spends one
token; if the bucket is empty, the request is rejected. This allows short
bursts (a full bucket) while capping the sustained rate (the refill rate).

YOUR TASK — implement `allow_request` so that:
1. Tokens refill lazily: on each call, compute how much time passed since the
   last refill and add `elapsed * refill_rate` tokens (float is fine).
2. The bucket never exceeds `capacity`.
3. If at least 1 token is available: spend one, return True.
4. Otherwise: return False (do NOT go negative).

Hints:
- You don't need a background thread. Lazy refill on access is the standard
  trick — same idea as TTL checks in caches.
- Track `self.tokens` (float) and `self.last_refill` (timestamp).
- The self-test injects a fake clock via `now_fn` so it runs instantly —
  always call `self.now_fn()` instead of `time.monotonic()` directly.

Run `python 02-rate-limiter.py` until the self-test passes.
"""

import time


class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float, now_fn=time.monotonic):
        """
        capacity:    max tokens the bucket holds (burst size)
        refill_rate: tokens added per second (sustained rate)
        now_fn:      clock function returning seconds (injectable for tests)
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.now_fn = now_fn
        self.tokens = float(capacity)  # start full
        self.last_refill = now_fn()

    def allow_request(self) -> bool:
        """Spend one token if available. Refill lazily based on elapsed time."""
        raise NotImplementedError("implement me — see module docstring")


# ---------------------------------------------------------------- self-test
if __name__ == "__main__":
    # Fake clock we can advance manually, so the test needs no real sleeping.
    clock = {"t": 0.0}
    fake_now = lambda: clock["t"]

    # Bucket: burst of 3, refills 1 token/second.
    bucket = TokenBucket(capacity=3, refill_rate=1.0, now_fn=fake_now)

    # Burst: a full bucket allows exactly `capacity` immediate requests.
    assert bucket.allow_request() is True
    assert bucket.allow_request() is True
    assert bucket.allow_request() is True
    assert bucket.allow_request() is False, "bucket empty — 4th request must be rejected"

    # After 1 second, exactly one token has dripped in.
    clock["t"] = 1.0
    assert bucket.allow_request() is True, "1 token refilled after 1s"
    assert bucket.allow_request() is False, "and only one"

    # Refill never exceeds capacity: after a long wait, still only 3 tokens.
    clock["t"] = 100.0
    assert bucket.allow_request() is True
    assert bucket.allow_request() is True
    assert bucket.allow_request() is True
    assert bucket.allow_request() is False, "capacity cap: long idle must not exceed burst size"

    # Fractional refill: 0.5s at 1 token/s = half a token — not enough.
    clock["t"] = 100.5
    assert bucket.allow_request() is False, "half a token is not a whole token"
    clock["t"] = 101.0
    assert bucket.allow_request() is True, "fractions accumulate to a full token"

    print("✅ all token-bucket tests passed")
