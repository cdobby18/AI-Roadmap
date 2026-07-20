# Phase 8 — Deploy + CI/CD + Portfolio

## Overview

Phase 8 ships the projects built in Phases 1–7 to production-like environments. The goal isn't just to host an app — it's to understand the full lifecycle: containerization, cloud deployment, CI/CD, environment management, and portfolio presentation.

## Core Concepts

### Docker

- **Image vs Container**: Image = blueprint (read-only). Container = running instance (writable layer).
- **Dockerfile**: `FROM` (base image), `WORKDIR` (working dir), `COPY` (add files), `RUN` (install deps), `CMD`/`ENTRYPOINT` (start command).
- **Layers**: Each instruction creates a layer. Docker caches layers — order matters. Put stable layers first (dependencies), volatile last (source code).
- **Multi-stage builds**: Build in one stage (with compilers), copy artifacts to a slim runtime stage. Reduces final image size by 10-100x.
- **.dockerignore**: Exclude `__pycache__/`, `.git/`, `.env` from the build context. Speeds up builds, prevents leaking secrets.
- **docker-compose.yml**: Define multi-service apps (e.g., app + vector DB + Redis cache). Single `docker compose up` starts everything.

### Deployment Platforms

| Platform | Free Tier | Best For | Limits |
|----------|-----------|----------|--------|
| **HuggingFace Spaces** | Yes | Streamlit/Gradio ML demos | 16GB storage, 2 vCPUs, no GPU on free |
| **Render** | Yes | Web services (FastAPI, Node) | 750 hrs/month, 512MB RAM |
| **Railway** | Yes (limited) | Full-stack apps | $5 credit, sleep after inactivity |
| **Fly.io** | Yes | Containerized apps worldwide | 3 shared VMs, 256MB RAM |

### CI/CD with GitHub Actions

- **Workflow**: YAML file in `.github/workflows/`. Triggered by push, PR, schedule.
- **Jobs**: Run in parallel by default. `needs:` creates dependency chains.
- **Steps**: Individual commands — checkout, setup Python, install deps, run tests.
- **Actions**: Reusable units from the marketplace (`actions/checkout`, `actions/setup-python`).
- **Matrix builds**: Test across multiple Python versions or OS in parallel.
- **Secrets**: Store API keys, tokens, passwords in GitHub Secrets → `${{ secrets.HF_TOKEN }}`.

### Environment Management

- **Never hardcode secrets** in code. Use environment variables.
- **`.env` files** for local dev (gitignored). Platform UI for production secrets.
- **Python**: `os.getenv("VAR", "default")` or `python-dotenv` for `.env` loading.

### Portfolio Best Practices

- **README**: Problem → Architecture → Setup → Demo link. Screenshots or GIFs.
- **Clean repo**: No `__pycache__`, `.DS_Store`, `.env`, large binaries. `.gitignore` is your first impression.
- **Demo link**: Deploy the app, add the URL to the README. A "Try it live" button beats 100 lines of docs.
- **One pinned project** that tells a story: data → model → app → deploy.

---

## Hands-On Files Reference

| File | What It Teaches |
|------|-----------------|
| `Dockerfile` | Multi-stage containerization for Streamlit + NLP models |
| `.dockerignore` | Build context hygiene |
| `huggingface-spaces/README.md` | HF Spaces config, secrets setup, push instructions |
| `.github/workflows/deploy-poneglyph.yml` | CI/CD — run tests, deploy to HF Spaces on push to main |

---

## Interview Must-Knows

- **Docker layer caching**: Explain why `COPY requirements.txt` before `RUN pip install` saves time.
- **Multi-stage builds**: Why not just `FROM python:3.12` for everything? Image size, attack surface.
- **CI/CD pipeline**: What should run on every PR (lint, test) vs every merge to main (deploy)?
- **Immutable infrastructure**: Why redeploy a new container instead of SSH'ing into production?
- **12-Factor App**: Config in env, no state in containers, log as streams.
- **Stateless vs stateful containers**: App servers are stateless (scale horizontally). Databases are stateful (persistent volumes needed).

## Key Tradeoffs

| Decision | Tradeoff |
|----------|----------|
| Docker vs manual setup | Reproducibility vs simplicity |
| HuggingFace Spaces vs Render | AI-specific portfolio vs general backend |
| GitHub Actions vs Jenkins | Managed simplicity vs enterprise control |
| Single service vs docker-compose | Simplicity vs realistic multi-service infra |
| Pre-built vs custom Dockerfile | Fast start vs understanding every layer |

---

## Deploy Checklist

- [ ] Choose a target platform (HF Spaces for Streamlit, Render for FastAPI)
- [ ] Write a Dockerfile, test locally with `docker build . && docker run`
- [ ] Add `.dockerignore` and `.gitignore`
- [ ] Set up CI/CD: tests on push, deploy on merge to main
- [ ] Add environment variables / secrets on the platform
- [ ] Update the project README with a live demo link
- [ ] Pin the repo on GitHub profile
