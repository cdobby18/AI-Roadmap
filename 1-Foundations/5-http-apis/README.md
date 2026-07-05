# 5 · HTTP & APIs

The `requests` library, end to end — this is the section that matters most day-to-day as an AI engineer, since every LLM API call (Anthropic, OpenAI, HF Inference) is an HTTP request under the hood.

---

## Progress Checklist

- [x] `request-1.py` — GET requests: `response.status_code`, `.text`, `.json()`, `.headers`; query params via `params=`; status code reference (200/201/400/401/404/500)
- [x] `request-2.py` — POST requests: `json=` payload (sets `Content-Type` automatically), a real call to the Anthropic Messages API with `.env`-loaded API key, plus `data=` and file-upload (`files=`) variants
- [x] `requests-3.py` — error handling: `try`/`except` around `requests.exceptions.Timeout`, `ConnectionError`, `HTTPError` (with status-code branching for 401/429), and a catch-all `RequestException`
- [x] `request-4.py` — headers & auth: building an `Authorization` header, then `requests.Session()` to persist headers/connections across multiple calls instead of repeating them
- [x] `sampleReq.py` — capstone: `AIClient` class wraps a `Session` + headers + error handling into one reusable `.chat(message)` method — this is the shape production API clients actually take

---

## Key Concepts

| Concept | One-liner |
|---------|-----------|
| `json=` vs `data=` | `json=` serializes and sets the header for you — prefer it for JSON APIs |
| `response.raise_for_status()` | Raises `HTTPError` on 4xx/5xx so you don't have to check `status_code` manually |
| `timeout=` | Always set one — an API call with no timeout can hang your program forever |
| `requests.Session()` | Reuses the TCP connection and shared headers — use it for chatbots/agents making repeated calls to the same API |
| 401 vs 429 | 401 = bad/missing API key; 429 = rate limited — different fixes, worth branching on |

---

## Note

File naming is inconsistent (`request-1`, `request-2`, `requests-3`, `request-4`) but the numbers are still the intended reading order; `sampleReq.py` is the unnumbered capstone that ties everything above into one class.
