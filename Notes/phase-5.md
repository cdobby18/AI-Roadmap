# Phase 5 - LLMs Notes

## Key Concepts

### Prompt Engineering
- **Zero-shot**: Direct question, no examples
- **Few-shot**: Provide examples before asking
- **Chain-of-thought**: Ask model to "think step by step"
- **System prompts**: Shape model behavior across all turns

### Parameters That Matter
- **Temperature** (0-1): 0=deterministic, 1=creative
- **Top_p**: Nucleus sampling, controls diversity
- **Max tokens**: Limit output length
- **Context window**: Total tokens model can see (varies by model)

### Function/Tool Calling
- Model decides WHEN to call functions
- Send schemas describing available tools
- Model returns function name + arguments
- Your code executes and returns results back

### Structured Outputs
- Force LLM to return valid JSON
- Include schema in prompt
- Parse and validate response
- Useful for data extraction, forms, etc.

### Context Engineering
- Token counting: ~1 token ≈ 4 characters
- Truncate old messages when context full
- Summarize old conversations to save tokens
- Plan for token budget before calling LLM

## LLM Providers

| Provider | Model | Cost | Speed | Quality |
|----------|-------|------|-------|---------|
| Ollama | llama2, mistral | Free | Fast | Good |
| OpenAI | GPT-4, GPT-3.5 | $$$ | Varies | Excellent |
| Anthropic | Claude | $$ | Good | Excellent |
| Google | Gemini | $ | Good | Good |

## Security Considerations
- Validate all user inputs
- Check for prompt injection patterns
- Rate limit requests
- Sanitize outputs
- Track costs & usage

## Observability
- Log: model, latency, tokens in/out, cost
- Track: errors, performance patterns
- Export: logs for analysis
- Monitor: per-user usage, API quotas

## Files Created
1. `01-ollama-basics.py` - API basics
2. `02-prompt-engineering.py` - Techniques
3. `03-function-calling.py` - Basic tools
4. `04-performance-comparison.py` - Model testing
5. `05-ollama-with-fastapi.py` - REST wrapper
6. `06-interactive-chatbot.py` - Interactive testing
7. `07-structured-outputs.py` - JSON responses
8. `08-tool-calling.py` - Advanced tools
9. `09-context-engineering.py` - Token management
10. `10-multiple-providers.py` - OpenAI, Anthropic, Gemini, Ollama
11. `11-security-prompt-injection.py` - Security
12. `12-observability-monitoring.py` - Tracking

## Next: Phase 6 (RAG)
- Embeddings & vector search
- Vector databases
- Document retrieval
- Building Q&A systems

Then Phase 7 (Advanced Frameworks)
- LangChain & LangGraph
- LangSmith & observability
- Guardrails & validation
- MCP protocol

Then Phase 8 (Deploy)
