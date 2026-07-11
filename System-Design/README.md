# System Design — Patterns in Code

Companion to [Notes/system-design-patterns.md](../Notes/system-design-patterns.md).
The notes hold the theory; this folder proves it in runnable Python.

The rule here: **a pattern isn't learned until it runs.** Each file is a small,
dependency-free implementation of one pattern, with a self-test at the bottom —
run it directly with `python <file>.py`.

## Patterns

| File | Pattern | Status |
|------|---------|--------|
| [01-lru-cache.py](01-lru-cache.py) | LRU cache eviction | ✅ Worked example |
| [02-rate-limiter.py](02-rate-limiter.py) | Token-bucket rate limiting | 🔨 Exercise |
| [03-consistent-hashing.py](03-consistent-hashing.py) | Consistent hashing ring | 🔨 Exercise |
| [04-circuit-breaker.py](04-circuit-breaker.py) | Circuit breaker + retry with backoff | 🔨 Exercise |
| [05-load-balancer.py](05-load-balancer.py) | Round-robin / least-connections LB | 🔨 Exercise |

`01-lru-cache.py` is fully implemented as the reference for style and testing.
The rest are guided exercises: each has the class skeleton, docstrings explaining
exactly what to build, and a self-test that fails until the implementation is right.
Implement, run, repeat until the self-test passes — then update the status here.

## Why these five

- **LRU cache** — the default eviction-policy answer in any caching question, and a classic interview implementation (hash map + doubly linked list, or `OrderedDict`).
- **Token-bucket rate limiter** — protects any API from overload; becomes real FastAPI middleware in Phase 7.
- **Consistent hashing** — why adding a cache node doesn't invalidate every key; underlies sharding and distributed caches.
- **Circuit breaker** — the pattern you'll wrap around every LLM API call in Phases 5–6; timeouts + retries alone still cascade.
- **Load balancer simulation** — makes round-robin vs least-connections concrete instead of a memorized definition.

## Forward connections

- Phase 5/6: circuit breaker + retry-with-backoff around LLM provider calls.
- Phase 6: consistent hashing intuition → vector DB sharding, Redis embedding cache.
- Phase 7: rate limiter as middleware in a deployed FastAPI service.
