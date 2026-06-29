# Phase 3 Project — BountyHunter

**Theme:** One Piece  
**Phase:** 3 — Machine Learning + PyTorch + Experiment Tracking  
**Prereqs:** Phase 1 (Python + OOP) · Phase 2 (FastAPI)

---

## What This Project Builds

A full ML pipeline that predicts a pirate's Marine-issued bounty (in millions of berries) from their crew stats. Covers every Phase 3 skill end-to-end.

---

## Project Files

| File | What it does | Phase 3 skill |
|------|--------------|---------------|
| `data.py` | Generates 1,000 synthetic pirates with NumPy, saves to CSV | NumPy, Pandas |
| `baseline.py` | Trains LinearRegression + RandomForest, prints MAE/R² | Classical ML, sklearn |
| `model.py` | Defines `BountyNet` — 3-layer PyTorch feedforward net | PyTorch `nn.Module` |
| `train.py` | Runs the training loop, logs metrics to W&B | PyTorch training loop, W&B |
| `evaluate.py` | Loads checkpoint, compares NN vs baselines on test set | Model evaluation |
| `app.py` | Gradio web UI — input pirate stats, get bounty prediction | Gradio, inference |

---

## Dataset Features

| Feature | Type | Range |
|---------|------|-------|
| `devil_fruit` | bool | 0 or 1 |
| `haki_level` | int | 0–3 |
| `crew_size` | int | 1–500 |
| `notoriety_score` | float | 0.0–10.0 |
| `region` | encoded int | 0=East Blue, 1=Grand Line, 2=New World |
| `bounty_berries` | float | target — millions |

No external dataset needed — generated programmatically in `data.py`.

---

## How to Run

```bash
# 1. Install dependencies (one-time)
pip install numpy pandas scikit-learn torch wandb gradio

# 2. Generate dataset
python data.py

# 3. Run sklearn baseline (sets the bar)
python baseline.py

# 4. Train PyTorch model (logs to W&B)
wandb login        # one-time: enter your API key
python train.py

# 5. Compare all models
python evaluate.py

# 6. Launch Gradio demo
python app.py
```

---

## The Training Loop (memorize this)

```python
for epoch in range(epochs):
    preds = model(X)              # 1. forward pass
    loss = loss_fn(preds, y)      # 2. compute loss
    optimizer.zero_grad()         # 3. clear old gradients
    loss.backward()               # 4. backprop
    optimizer.step()              # 5. update weights
```

This exact pattern — forward → loss → zero_grad → backward → step — is used in every PyTorch training job, from toy models to fine-tuning LLMs.

---

## What to Look For

- **baseline.py** prints MAE for LinearRegression and RandomForest. Note them.
- **train.py** logs train/val RMSE and val MAE to your W&B dashboard every epoch. Open the W&B link to see the learning curve.
- **evaluate.py** prints a side-by-side comparison. The NN should beat LinearRegression in MAE (the dataset has nonlinear relationships). RandomForest may still compete — that's expected and shows when tree-based models are hard to beat.
- **app.py** launches at `http://localhost:7860`. Try the preset examples: a New World pirate with Haki 3 and a Devil Fruit vs. an East Blue rookie.

---

## Phase 3 Skills Demonstrated

- [x] NumPy vectorized operations (data.py)
- [x] Pandas DataFrame + CSV I/O (data.py)
- [x] sklearn `fit` / `predict` pattern (baseline.py)
- [x] Train/test split + StandardScaler (baseline.py, train.py)
- [x] RandomForest (baseline.py)
- [x] PyTorch `nn.Module` with `nn.Sequential` (model.py)
- [x] Full training loop with mini-batches (train.py)
- [x] MAE, R² evaluation metrics (evaluate.py)
- [x] W&B experiment tracking (train.py)
- [x] Gradio model deployment (app.py)

---

## Bridge to Phase 4

The `01-huggingface-pipeline.py` in `3-ML/6-ml-tools/` runs a SOTA NLP model in 3 lines. After completing this project, the next step is Phase 4: understanding *why* those pre-trained models work — tokenization, embeddings, attention, BERT/GPT.

The trained `BountyNet` checkpoint could also be served as a FastAPI endpoint (Phase 5 bridge): load the model at startup with `Depends()`, accept pirate stats via a Pydantic schema, return the prediction — exactly the pattern from Phase 2.
