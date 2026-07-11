"""
Circuit Breaker — guided exercise.

Theory: Notes/system-design-patterns.md -> "circuit breaker", "retry with
backoff", "timeout".

The problem: a dependency (an LLM API, another service) starts failing.
Naive retries pile up waiting requests and make the outage worse. A circuit
breaker fails FAST once it knows the dependency is down, then probes
periodically to see if it recovered.

Three states:
- CLOSED    : normal operation. Calls pass through. Count consecutive
              failures; at `failure_threshold`, trip to OPEN.
- OPEN      : reject calls immediately (raise CircuitOpenError) WITHOUT
              calling the dependency. After `recovery_timeout` seconds,
              the next call is allowed through as a probe -> HALF_OPEN.
- HALF_OPEN : one probe call in flight. Success -> CLOSED (reset counters).
              Failure -> back to OPEN (restart the recovery timer).

YOUR TASK — implement `call(fn)` so the state machine above holds:
1. CLOSED: run fn(). On success, reset the failure count and return the
   result. On exception, increment failures; if failures reach
   `failure_threshold`, record the trip time and move to OPEN. Re-raise.
2. OPEN: if less than `recovery_timeout` has passed since tripping, raise
   CircuitOpenError WITHOUT calling fn. Otherwise move to HALF_OPEN and
   treat this call as the probe.
3. HALF_OPEN: run fn(). Success -> CLOSED, reset everything, return result.
   Exception -> OPEN, reset the recovery timer, re-raise.

Hints:
- Like the rate limiter, use `self.now_fn()` for time so the test's fake
  clock works.
- Track: state, consecutive failure count, and when the circuit opened.

Run `python 04-circuit-breaker.py` until the self-test passes.
"""

import time

CLOSED, OPEN, HALF_OPEN = "closed", "open", "half_open"


class CircuitOpenError(Exception):
    """Raised when the breaker rejects a call without trying the dependency."""


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: float = 30.0,
                 now_fn=time.monotonic):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.now_fn = now_fn
        self.state = CLOSED
        # TODO: your counters/timestamps here

    def call(self, fn):
        """Invoke fn() through the breaker, enforcing the state machine."""
        raise NotImplementedError("implement me — see module docstring")


# ---------------------------------------------------------------- self-test
if __name__ == "__main__":
    clock = {"t": 0.0}
    fake_now = lambda: clock["t"]

    calls = {"n": 0}

    def flaky(fail: bool):
        def fn():
            calls["n"] += 1
            if fail:
                raise ConnectionError("dependency down")
            return "ok"
        return fn

    br = CircuitBreaker(failure_threshold=3, recovery_timeout=30.0, now_fn=fake_now)

    # CLOSED: successes pass through, failures count.
    assert br.call(flaky(False)) == "ok"
    assert br.state == CLOSED

    for i in range(3):
        try:
            br.call(flaky(True))
            raise AssertionError("failure must re-raise the original error")
        except ConnectionError:
            pass
    assert br.state == OPEN, "3rd consecutive failure must trip the breaker"

    # OPEN: fail fast — the dependency must NOT be called.
    n_before = calls["n"]
    try:
        br.call(flaky(True))
        raise AssertionError("open breaker must raise CircuitOpenError")
    except CircuitOpenError:
        pass
    assert calls["n"] == n_before, "open breaker must not touch the dependency"

    # After recovery_timeout, one probe goes through. It fails -> OPEN again.
    clock["t"] = 31.0
    try:
        br.call(flaky(True))
    except ConnectionError:
        pass
    assert br.state == OPEN, "failed probe reopens the circuit"

    # Timer restarted: still open at t=32 even though 31 > original trip + 30...
    try:
        br.call(flaky(False))
        raise AssertionError("recovery timer must restart after a failed probe")
    except CircuitOpenError:
        pass

    # Probe succeeds after another full recovery window -> CLOSED.
    clock["t"] = 62.0
    assert br.call(flaky(False)) == "ok"
    assert br.state == CLOSED, "successful probe closes the circuit"

    # Failure count was reset on recovery: 2 failures don't re-trip.
    for _ in range(2):
        try:
            br.call(flaky(True))
        except ConnectionError:
            pass
    assert br.state == CLOSED, "counters must reset when the circuit closes"

    print("✅ all circuit-breaker tests passed")
