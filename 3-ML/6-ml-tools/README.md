# 6 · ML Tools

The tools that turn experiments into real products — Hugging Face for pre-trained models, W&B for experiment tracking, Gradio for demos.

---

## What You'll Learn

- **Hugging Face `pipeline()`** — run state-of-the-art models in 3 lines
- **Weights & Biases (W&B)** — track metrics, compare runs, visualize training
- **Gradio** — wrap any model in a shareable web UI in under 10 lines

---

## Progress Checklist

- [ ] `01-huggingface-pipeline.py` — sentiment analysis, text generation, zero-shot
- [ ] `02-wandb-basics.py` — log metrics during a PyTorch training run
- [ ] `03-gradio-demo.py` — build and launch a sentiment classifier UI

---

## Setup

```bash
pip install transformers torch wandb gradio
wandb login   # get your API key from wandb.ai
```

---

## Key Concepts

| Tool | What it does |
|------|--------------|
| `pipeline("task")` | Loads a pre-trained model for a given task — no training needed |
| `wandb.init()` | Start tracking a new run |
| `wandb.log({"loss": val})` | Log any metric at any point in training |
| `gr.Interface(fn, inputs, outputs)` | Wraps a Python function in a web UI |
| `demo.launch()` | Starts a local server at localhost:7860 |

---

## Resources

| Resource | What |
|----------|------|
| Hugging Face — Pipeline tutorial | How to run pre-trained models |
| Weights & Biases quickstart | Set up W&B in 5 minutes |
| Gradio docs (gradio.app) | Quickstart only — all you need |
