# BountyHunter — Phase 3 ML Capstone

> One Piece themed · Phase 3: Machine Learning + PyTorch + Experiment Tracking

---

## What This Is

A complete ML pipeline that predicts a pirate's Marine-issued bounty (in millions of berries) from their crew stats. Every Phase 3 skill is applied here — from NumPy data generation to a trained PyTorch model deployed in a Gradio web UI.

**Series:** Phase 1 → Devil Fruit Database · Phase 2 → Grand Line API · **Phase 3 → BountyHunter**

---

## Quick Start

```bash
pip install numpy pandas scikit-learn torch wandb gradio

python data.py       # generate pirates.csv
python baseline.py   # run sklearn benchmarks
wandb login          # one-time API key setup
python train.py      # train PyTorch model
python evaluate.py   # compare all models
python app.py        # launch Gradio UI → http://localhost:7860
```

---

## Files

| File | Purpose |
|------|---------|
| `data.py` | Generate 1,000 synthetic pirates with NumPy, save to `pirates.csv` |
| `baseline.py` | LinearRegression · RandomForest · **XGBoost** · **Cross-validation** · **GridSearchCV** |
| `model.py` | `BountyNet` — PyTorch 3-layer feedforward network |
| `train.py` | Training loop + W&B experiment tracking |
| `evaluate.py` | Part A: regression (MAE, R²) · Part B: **confusion matrix, precision, recall, F1, AUC-ROC** |
| `app.py` | Gradio web UI — input stats, get predicted bounty |
| `project.md` | Full spec, run instructions, skill checklist |

---

## Study Notes

### NumPy — Why It Matters

NumPy is the foundation of all ML in Python. Every library (pandas, sklearn, PyTorch, TensorFlow) speaks NumPy under the hood.

**Key concepts to know:**
- `np.array` vs Python list — NumPy arrays are stored in contiguous memory and support vectorized operations (no for loops needed)
- **Broadcasting** — operations between arrays of different shapes: `arr * 2` multiplies every element
- **Vectorized ops** — `arr.mean()`, `arr.std()`, `arr.sum()` operate on the whole array at C speed
- `dtype` matters — ML always uses `float32` (half the memory of `float64`, good enough for training)

```python
# This is how data.py generates the dataset — no loops
bounty = devil_fruit * 200 + haki_level * 150 + crew_size * 0.8 + noise
```

---

### Pandas — The Data Wrangling Layer

Pandas wraps NumPy arrays in labeled columns (DataFrames). Every ML project starts with a DataFrame.

**Key concepts:**
- `df[col]` → Series (one column), `df[[cols]]` → DataFrame (multiple)
- `df.describe()` → quick stats: count, mean, std, min, max, quartiles
- `df.to_csv()` / `pd.read_csv()` — save and load data
- `df[FEATURES].values` → back to NumPy array for sklearn/PyTorch

---

### sklearn — The Universal ML Interface

sklearn's pattern is the same for every algorithm:
```python
model = SomeAlgorithm()     # 1. instantiate
model.fit(X_train, y_train) # 2. train
preds = model.predict(X)    # 3. infer
```

**Key concepts:**
- `train_test_split` — always split BEFORE fitting. If you fit on the full dataset, your evaluation metrics are lies.
- `StandardScaler` — transforms each feature to mean=0, std=1. Required for linear models and neural networks. Tree-based models (RF, XGBoost) don't need it.
- `mean_absolute_error` — average of |pred - true|. Interpretable: "off by X berries on average"
- `r2_score` — how much variance the model explains. 1.0 = perfect, 0.0 = no better than predicting the mean, negative = worse than the mean

**XGBoost** — gradient boosting that builds trees sequentially, each one correcting the errors of the last. Often the strongest classical model on tabular data and a common interview topic.
```python
from xgboost import XGBRegressor
xgb = XGBRegressor(n_estimators=100, learning_rate=0.1)
xgb.fit(X_train, y_train)
```

**Cross-Validation** — instead of one train/test split (which can be lucky or unlucky), CV splits the data K times and averages the score. Always more reliable than a single split.
```python
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=5, scoring="neg_mean_absolute_error")
print(-scores.mean())  # average MAE across 5 folds
```

**GridSearchCV** — exhaustively tries every combination of hyperparameters and picks the best using cross-validation.
```python
from sklearn.model_selection import GridSearchCV
grid = GridSearchCV(RandomForest(), {"n_estimators": [50, 100], "max_depth": [None, 10]}, cv=3)
grid.fit(X_train, y_train)
print(grid.best_params_)
```

---

### PyTorch — Building Neural Networks

PyTorch is the framework used in production AI engineering and research. The three things to know cold:

#### 1. `nn.Module` — Base class for every model

```python
class BountyNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(5, 64),  # 5 inputs → 64 hidden units
            nn.ReLU(),         # activation: max(0, x)
            nn.Linear(64, 1),  # → 1 output (bounty)
        )

    def forward(self, x):
        return self.net(x).squeeze(-1)
```

#### 2. Tensors — PyTorch's data type

PyTorch tensors are like NumPy arrays but can run on GPU and track gradients.
```python
x = torch.tensor([[1.0, 2.0, 3.0]])  # shape (1, 3)
x.shape    # torch.Size([1, 3])
x.dtype    # torch.float32
```

#### 3. The Training Loop — memorize this

```python
for epoch in range(epochs):
    preds = model(X)              # forward pass
    loss = loss_fn(preds, y)      # compute loss (MSE for regression)
    optimizer.zero_grad()         # MUST clear old gradients first
    loss.backward()               # backprop: compute gradients
    optimizer.step()              # update weights
```

**Why `zero_grad()` before `backward()`?**  
PyTorch *accumulates* gradients by default. If you skip `zero_grad()`, gradients from the previous batch get added to the new ones — the model learns garbage.

---

### Model Evaluation

#### Regression Metrics (Part A)
| Metric | Formula | When to use |
|--------|---------|-------------|
| MAE | mean(\|pred - true\|) | Interpretable — same units as the target |
| RMSE | sqrt(mean((pred - true)²)) | Penalizes large errors more than MAE |
| R² | 1 - SS_res/SS_tot | Proportion of variance explained (1.0 = perfect) |

#### Classification Metrics (Part B — evaluate.py)
| Metric | Formula | When to use |
|--------|---------|-------------|
| Accuracy | correct / total | Only reliable when classes are balanced |
| Precision | TP / (TP + FP) | Minimize false positives (e.g., spam filter — don't block legit mail) |
| Recall | TP / (TP + FN) | Minimize false negatives (e.g., disease detection — don't miss sick patients) |
| F1 | 2 × P×R / (P+R) | Balance of precision and recall; use on imbalanced datasets |
| AUC-ROC | area under ROC curve | Model discrimination regardless of decision threshold; 0.5 = random |

**Confusion Matrix** — the most important tool for classification debugging:
```
              Predicted 0    Predicted 1
  Actual 0  [    TN              FP    ]   ← False Positive = false alarm
  Actual 1  [    FN              TP    ]   ← False Negative = missed detection
```

**Rule of thumb:** if false negatives are dangerous (missing a disease, missing fraud), optimize for **Recall**. If false positives are costly (flagging innocent users, blocking valid emails), optimize for **Precision**. When you need both, use **F1**. When you're comparing two models without committing to a threshold, use **AUC-ROC**.

For this project: **MAE** is the main regression metric. The classifier in Part B shows the pattern you'll use on any classification task.

---

### W&B — Experiment Tracking

W&B (Weights & Biases) lets you log metrics from any training run and compare them visually.

```python
import wandb

wandb.init(project="bountyhunter", config={"lr": 1e-3, "epochs": 100})

for epoch in range(epochs):
    ...
    wandb.log({"train_loss": loss, "val_mae": mae})

wandb.finish()
```

After running `train.py`, go to [wandb.ai](https://wandb.ai) → your project → see loss curves. Run it twice with different hyperparameters to compare runs. This is the workflow every ML team uses.

---

### Gradio — Ship Your Model in 10 Lines

Gradio wraps any Python function into a shareable web app.

```python
import gradio as gr

def predict(devil_fruit, haki_level, crew_size, notoriety, region):
    # ... model inference ...
    return f"Bounty: {bounty:.0f}M berries"

gr.Interface(fn=predict, inputs=[...], outputs="text").launch()
```

This is how demo.py at HuggingFace Spaces works. Your trained model becomes a live URL you can share with anyone.

---

## What the Numbers Should Look Like

After running all scripts, you should see something like:

```
=== Model Comparison (test set) ===

LinearRegression      MAE ~30.0     R² ~0.91
RandomForest          MAE ~28.0     R² ~0.93
BountyNet (PyTorch)   MAE ~29.0     R² ~0.92
```

The dataset is nearly linear (by design), so RF and the NN will be close. The goal is to see the NN in the same ballpark — not to "win" but to verify the training loop worked correctly.

---

## Connects To

- **Phase 4** — The HuggingFace `pipeline()` in `3-ML/6-ml-tools/01-huggingface-pipeline.py` runs a pre-trained transformer in 3 lines. Phase 4 explains why transformers work: tokenization, embeddings, attention.
- **Phase 5** — Serve `BountyNet` as a FastAPI endpoint. Load the model via `Depends()`, accept input via a Pydantic schema, return prediction as JSON. Same architecture as `phase-2-grandlineAPI`.
