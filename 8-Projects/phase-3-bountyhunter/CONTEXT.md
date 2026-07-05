# BountyHunter — Context

**Phase:** 3 — Machine Learning + PyTorch + Experiment Tracking
**Theme:** Predict a pirate's Marine-issued bounty (in millions of berries) from their crew stats.

**Series:** Phase 1 → Devil Fruit Database · Phase 2 → Grand Line API · **Phase 3 → BountyHunter**

---

## What This Builds

A full ML pipeline covering every Phase 3 skill end-to-end: synthetic data generation → classical ML baselines → a PyTorch neural net → experiment tracking → model comparison → a Gradio demo.

---

## Files

| File | What It Does |
|---|---|
| `data.py` | Generates 1,000 synthetic pirates with NumPy, saves to `pirates.csv` |
| `baseline.py` | Trains LinearRegression, RandomForest, XGBoost; runs cross-validation and GridSearchCV |
| `model.py` | Defines `BountyNet` — a 3-layer PyTorch feedforward net (`nn.Module` + `nn.Sequential`) |
| `train.py` | Runs the training loop, logs metrics to Weights & Biases |
| `evaluate.py` | Loads the checkpoint; Part A compares NN vs baselines on regression metrics, Part B runs classification metrics (confusion matrix, precision/recall/F1/AUC-ROC) |
| `app.py` | Gradio web UI — input pirate stats, get a bounty prediction |

---

## Dataset Features (`pirates.csv`)

| Feature | Type | Range |
|---|---|---|
| `devil_fruit` | bool | 0 or 1 |
| `haki_level` | int | 0–3 |
| `crew_size` | int | 1–500 |
| `notoriety_score` | float | 0.0–10.0 |
| `region` | encoded int | 0=East Blue, 1=Grand Line, 2=New World |
| `bounty_berries` | float | target — millions |

Fully synthetic — no external dataset needed. `data.py` generates it directly with NumPy vectorized operations (no loops):

```python
bounty = devil_fruit * 200 + haki_level * 150 + crew_size * 0.8 + noise
```

---

## How to Run

```bash
pip install numpy pandas scikit-learn xgboost torch wandb gradio

python data.py       # generate pirates.csv
python baseline.py   # sklearn benchmarks (LinearRegression, RandomForest, XGBoost, CV, GridSearchCV)
wandb login          # one-time API key setup
python train.py      # train PyTorch model, logs to W&B
python evaluate.py   # compare all models
python app.py        # Gradio UI → http://localhost:7860
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

Forward → loss → zero_grad → backward → step — this exact pattern shows up in every PyTorch training job, from this toy model to fine-tuning LLMs.

---

## What the Numbers Should Look Like

```
=== Model Comparison (test set) ===

LinearRegression      MAE ~30.0     R² ~0.91
RandomForest          MAE ~28.0     R² ~0.93
BountyNet (PyTorch)   MAE ~29.0     R² ~0.92
```

The dataset is nearly linear by design, so RF and the NN land close together — the goal is verifying the training loop worked, not "winning" against the baselines.

- `baseline.py` prints MAE for LinearRegression and RandomForest — note them before training the NN.
- `train.py` logs train/val RMSE and val MAE to the W&B dashboard every epoch.
- `evaluate.py` prints the side-by-side comparison; the NN should beat LinearRegression (nonlinear relationships in the data) — RandomForest may still compete, which is expected.
- `app.py` launches at `http://localhost:7860`; try a New World pirate with Haki 3 and a Devil Fruit vs. an East Blue rookie.

---

## Phase 3 Skills Demonstrated

- [x] NumPy vectorized operations (`data.py`)
- [x] Pandas DataFrame + CSV I/O (`data.py`)
- [x] sklearn `fit`/`predict` pattern (`baseline.py`)
- [x] Train/test split + `StandardScaler` (`baseline.py`, `train.py`)
- [x] RandomForest, XGBoost, cross-validation, GridSearchCV (`baseline.py`)
- [x] PyTorch `nn.Module` with `nn.Sequential` (`model.py`)
- [x] Full training loop with mini-batches (`train.py`)
- [x] Regression metrics: MAE, R² (`evaluate.py`)
- [x] Classification metrics: confusion matrix, precision, recall, F1, AUC-ROC (`evaluate.py`)
- [x] W&B experiment tracking (`train.py`)
- [x] Gradio model deployment (`app.py`)
