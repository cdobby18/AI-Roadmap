# Phase 5 · LLMs + Prompting + Observability

---

## What You'll Learn

- **Tokens vs Words** — LLMs think in tokens. Know how to estimate token count, why it affects cost, and what a context window limit actually means.
- **Temperature & Sampling** — what temperature controls, when to set it low (factual tasks) vs high (creative tasks). Know `top_p` and `top_k` at a surface level.
- **Prompting Techniques** — zero-shot, few-shot, chain-of-thought (CoT), system prompts. Know when to use each and why. CoT alone can dramatically improve reasoning output.
- **Function / Tool Calling** — let the LLM decide when to call a function. This is how agents are built. Understand the request/response cycle.
- **Structured JSON Output** — force the model to return structured data using system prompts or response format parameters. Critical for building reliable AI pipelines.
- **Streaming Responses** — return tokens as they're generated instead of waiting for the full response. Required for any chat interface.
- **LangSmith Tracing** — trace every LLM call: inputs, outputs, latency, token usage. Production systems are blind without this.
- **Prompt Injection Defense** — understand the attack, know the basic mitigations. Sanitize user input before it touches a system prompt.
- **Local LLMs with Ollama** — run `llama3`, `mistral`, or `phi3` locally. Free, private, useful for development and testing.

---

## Resources

| Resource | What You Get | Format | Cost |
|----------|-------------|--------|------|
| Anthropic — Prompt Engineering Guide | Best prompting reference from the model creators. Read all of it. | Docs | Free |
| OpenAI — Prompt Engineering Guide | Complements Anthropic's guide. Covers function calling well. | Docs | Free |
| LangSmith docs (smith.langchain.com) | Set up tracing in 10 minutes. Do this on day one of the phase. | Docs | Free |
| Ollama (ollama.com) | Run LLMs locally. Pull `llama3` or `mistral` and test locally. | Tool | Free |
| Simon Willison — Prompt Injection blog | The best plain-English explanation of prompt injection risks. | Blog | Free |
| Hamel Husain — LLM Evals blog | How to evaluate LLM outputs beyond vibes. Practical and real. | Blog | Free |

---
