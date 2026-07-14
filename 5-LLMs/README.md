# Phase 5 — LLMs + Prompt Engineering + Observability

**Status: ✅ Complete**

Working with large language models as an engineer.

## Quick Start

1. Start Ollama: `ollama serve`
2. Install model: `ollama pull llama2`
3. Run chatbot: `python 06-interactive-chatbot.py`

## What You'll Learn

**Prompt Engineering**
- Zero-shot, few-shot, chain-of-thought prompting
- System prompts & behavior shaping
- Temperature, context windows, token optimization

**Function & Tool Calling**
- Basic: LLM decides when to call functions
- Advanced: Tool schemas & multi-turn orchestration

**Structured Outputs**
- Force valid JSON responses
- Schema validation & data extraction

**Context Engineering**
- Token counting & management
- Handling long conversations
- Optimization strategies

**Multiple Providers**
- OpenAI (GPT-3.5, GPT-4)
- Anthropic (Claude)
- Google Gemini
- Local: Ollama (llama2, mistral, etc.)

**Security & Observability**
- Prompt injection detection
- Input validation & sanitization
- Performance tracking & cost monitoring

## Files

### Foundation (Start Here)
| File | Topic |
|------|-------|
| `01-ollama-basics.py` | Basic API & chat |
| `06-interactive-chatbot.py` | **⭐ Interactive testing** |

### Prompt Engineering & Techniques
| File | Topic |
|------|-------|
| `02-prompt-engineering.py` | Prompting strategies |
| `03-function-calling.py` | Basic tool calling |
| `07-structured-outputs.py` | JSON validation |
| `08-tool-calling.py` | Advanced tools |

### Advanced Topics
| File | Topic |
|------|-------|
| `09-context-engineering.py` | Token management |
| `10-multiple-providers.py` | All LLM providers |
| `11-security-prompt-injection.py` | Security & validation |
| `12-observability-monitoring.py` | Tracking & metrics |

### Integration
| File | Topic |
|------|-------|
| `04-performance-comparison.py` | Model benchmarks |
| `05-ollama-with-fastapi.py` | REST API |

## Key Parameters

| Parameter | Range | Default | Effect |
|-----------|-------|---------|--------|
| `temperature` | 0-1 | 0.7 | 0=focused, 1=creative |
| `top_p` | 0-1 | 0.9 | Diversity sampling |
| `max_tokens` | 1+ | 128 | Output length |

## Tips

- **First call takes 30-60s** (model loads into memory)
- **Use mistral or orca-mini for faster testing**
- **Ollama runs on localhost:11434**
- **Token estimate: ~4 characters = 1 token**

## Coverage

✅ Prompt engineering (all strategies)
✅ Function & tool calling
✅ Structured outputs (JSON)
✅ Context & token management
✅ Multiple LLM providers
✅ Security & prompt injection
✅ Observability & monitoring
✅ Interactive chatbot

## Next: Phase 6 (RAG)

Ready to build with external data?

**Phase 6 covers:**
- Embeddings & vector similarity
- Vector databases (Pinecone, FAISS, Weaviate)
- Document retrieval & indexing
- Building Q&A systems over your data
- RAG + LangChain integration

See: [6-RAG/README.md](../6-RAG/README.md)