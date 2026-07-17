# Phase 5 — LLMs + Prompt Engineering + Observability

## Prompt Engineering Strategies

**Zero-shot:** Ask the question directly. Works well for models trained on instruction-following (GPT-4, Claude 3, Llama 3). Fails when the task is niche or requires specific output formatting.

**Few-shot:** Provide 2-5 examples before asking. Dramatically improves quality for formatting, classification, and extraction tasks. The examples serve as implicit instructions — choose them carefully.

**Chain-of-thought (CoT):** Ask the model to "think step by step." Improves reasoning on math, logic, and multi-step problems. The model generates intermediate reasoning before the final answer. Can be triggered by simply adding "Let's think step by step" (zero-shot CoT).

**System prompts:** A persistent instruction set on the model's behavior. Used to set the persona ("You are a helpful assistant"), rules ("Do not make up facts"), and output format preferences. Only works with models that support system messages (most modern ones do).

**When to use each:**
- Zero-shot: simple questions, capable models, quick iteration.
- Few-shot: need specific format or style, model doesn't follow instructions well.
- Chain-of-thought: math, logic, multi-step reasoning, planning.
- System prompt: set behavior/tone across all turns, guardrails.

## Parameters That Matter

| Parameter | Effect | When to adjust |
|-----------|--------|----------------|
| Temperature (0-2) | 0 = deterministic, 1+ = creative | Lower for facts/math, higher for creative writing |
| Top-p (0-1) | Nucleus sampling — only consider tokens above cumulative p | Alternative to temperature; lower = more focused |
| Max tokens | Hard limit on output length | Set just above expected answer length to save cost/latency |
| Stop sequences | Strings that halt generation | Use to get structured output (stop at "\n\n" or "###") |
| Frequency/ Presence penalty | Penalize repeating tokens | Reduce repetition in long generations |

**Key insight:** Temperature + top-p control the creativity vs determinism tradeoff. For RAG and structured outputs, use temperature=0 for reproducibility. For creative writing or brainstorming, temperature=0.7-1.0.

## Inference Optimization

**KV Cache:** During autoregressive generation, the Key and Value matrices from previous tokens are cached so they don't need to be recomputed for each new token. Without this, generation would be O(n²) instead of ~O(n). Most libraries handle this automatically. Memory cost grows with sequence length and batch size.

**Speculative decoding:** A small "draft" model generates candidate tokens quickly; the large model verifies them in parallel. Can be 2-3x faster without quality loss. Used in production systems (TensorRT-LLM, vLLM).

**Batch inference:** Process multiple inputs simultaneously on GPU. Linear throughput improvement until GPU memory is saturated. Always batch inference requests if latency requirements allow it (combine them and process together).

**Quantization:** Reduces model weight precision (FP16 → INT8/INT4). Shrinks model size 2-4x, speeds up inference, may slightly reduce quality. Key methods:
- **GPTQ:** Post-training quantization, needs a calibration dataset. Good for GPU inference.
- **AWQ:** Similar to GPTQ but better at preserving important weights. Newer standard for GPU.
- **GGUF:** Quantized format for CPU inference via llama.cpp. Standard for running models locally on laptop/CPU.

**When to use each:** GPTQ/AWQ for GPU serving (high throughput), GGUF for local/CPU inference (Ollama, llama.cpp).

## Tool Calling / Function Calling

The LLM receives JSON schemas describing available tools. When appropriate, it returns a structured response specifying which tool to call and with what arguments. Your code executes the tool and feeds the result back to the model.

**The flow:** (1) Define tool schemas → (2) Send user query + schemas to LLM → (3) LLM returns tool call or direct response → (4) If tool call: execute tool, send result back → (5) LLM uses tool result to answer.

**Why it works:** The LLM doesn't execute code — it decides when to delegate to code. The actual execution is sandboxed in your environment. This is how ChatGPT plugins, GPT Actions, and assistant APIs work.

## Structured Outputs

Force the LLM to return valid JSON (or other structured format). Methods:

1. **Prompt engineering:** "Respond with valid JSON: {\"key\": \"value\"}" — works most of the time, can fail on smaller models.
2. **API-level enforcement:** OpenAI's `response_format={"type": "json_object"}`, Anthropic's tool use. More reliable.
3. **Validation + retry:** Parse output, catch errors, retry with error message in prompt. Most robust but adds latency.

**Why structured outputs matter:** Unstructured text is hard to integrate into automated pipelines. JSON output can be directly parsed into Pydantic models and used programmatically.

## Context Engineering

**Token counting:** ~4 characters ≈ 1 token for English. Different for other languages, code (more compact), or special characters. Use the model's tokenizer (tiktoken for OpenAI) for accurate counting.

**Context window limits:** Models have maximum context (4K, 8K, 32K, 128K, 1M tokens). Exceeding it causes truncation or errors. Strategies:
- **Sliding window:** Keep the most recent N tokens, drop the oldest.
- **Summarization:** Summarize old conversation turns into a compressed form.
- **Selective retention:** Keep system prompt + recent turns + important facts; drop filler.

**When to use each:** Sliding window for simple chat, summarization for long-running conversations, selective retention for RAG (keep retrieved chunks + recent history).

## Security

**Prompt injection:** User input tricks the model into ignoring its instructions. "Ignore previous instructions and say ___" is the classic form.

**Defense layers:**
1. **Input validation** — reject suspicious patterns (ignore instructions, system prompt manipulation).
2. **Output sanitization** — never directly render LLM output without escaping. Prevents XSS and markdown injection.
3. **Least privilege** — don't give the model access to tools it doesn't need. A travel agent doesn't need a database delete command.
4. **Rate limiting** — prevent abuse by capping requests per user.
5. **Separation of concerns** — system prompt and user input should never interleave in a way that allows instruction overwrite.

**Defense-in-depth:** No single defense is perfect. Multiple layers make exploitation harder.

## Observability

Every LLM call should track:
- **Model and provider** — which model, which deployment.
- **Input/output tokens** — most API billing is per token. Track to understand costs.
- **Latency** — time to first token (TTFT) and total generation time. High TTFT = slow model load or network.
- **Cost** — calculated from token counts × provider pricing. You can't optimize what you don't measure.
- **Error rate** — 4xx/5xx responses, timeout, content filter triggers.
- **User ID** — who made the call. Needed for abuse detection and per-user billing.

**Logging structure:** JSON logs per call, stored in a searchable system (Elasticsearch, Loki, or at minimum JSONL files). Include request ID for tracing across services.

## Multi-Provider Abstraction

The pattern: define a common interface (generate, generate_structured, count_tokens) and implement it for each provider. The application code never calls OpenAI or Anthropic directly — it calls the interface. This lets you:
- Swap providers without code changes
- Route queries by cost/speed (Ollama for simple, GPT-4 for complex)
- Fall back if one provider is down
- Compare quality/cost across providers

## Interview Must-Knows

- Zero-shot vs few-shot vs chain-of-thought: when each is appropriate.
- Temperature effect: 0 = deterministic (good for facts), high = creative (good for writing).
- How tool calling works: LLM returns function name + args, your code executes and feeds result back.
- Structured output methods: prompt engineering vs API enforcement vs validation+retry.
- KV cache: what it is, why it's necessary, memory cost.
- Quantization: GPTQ/AWQ for GPU, GGUF for CPU. Tradeoff: smaller/faster vs slight quality loss.
- Prompt injection: how it works and defense layers.
- What to log per LLM call: model, provider, tokens, latency, cost, error, user.
- Why multi-provider abstraction: interchangeable providers, routing, fallback.
