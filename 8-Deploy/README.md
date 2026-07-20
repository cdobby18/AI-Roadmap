# Phase 8 — Deploy + CI/CD + Portfolio

**Status: ✅ In Progress**

Shipping roadmap projects to production-like environments.

## What's Here

| File | Purpose |
|------|---------|
| `Dockerfile` | Containerize the Poneglyph Reader (multi-stage, slim) |
| `.dockerignore` | Exclude caches, git, env from build context |
| `huggingface-spaces/README.md` | Deploy guide — HF Spaces setup, secrets, push |
| `huggingface-spaces/.gitattributes` | Language detection for HF Spaces |

## Projects Deployed

| Project | Platform | URL | Status |
|---------|----------|-----|--------|
| Poneglyph Reader (Phase 6) | HuggingFace Spaces | TBD | 🟡 Ready to deploy |

## CI/CD

| Workflow | Trigger | Action |
|----------|---------|--------|
| `deploy-poneglyph.yml` | Push to `main` (Poneglyph files) | Tests → Deploy to HF Spaces |

## Running Locally with Docker

```bash
cd Projects/phase-6-poneglyph
docker build -t poneglyph-reader -f ../../8-Deploy/Dockerfile .
docker run -p 7860:7860 poneglyph-reader
```

## Phase Contents

- **Docker**: Multi-stage Dockerfile for Streamlit + NLP models
- **HuggingFace Spaces**: One-click deploy of AI demos
- **GitHub Actions**: Automated tests + deploy pipeline
- **Environment management**: Secrets, env vars, `.env` patterns
- **Portfolio**: Live demo links, polished READMEs
