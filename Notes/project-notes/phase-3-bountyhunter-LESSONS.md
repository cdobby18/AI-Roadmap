# BountyHunter — Lessons

**Phase:** 3 — Machine Learning + PyTorch + Experiment Tracking

---

## NumPy — Why It Matters

NumPy underlies pandas, sklearn, and PyTorch. Key ideas exercised here: `np.array` vs Python list (contiguous memory, vectorized ops, no loops needed), **broadcasting** (`arr * 2` applies to every element), vectorized aggregates (`.mean()`, `.std()`, `.sum()` at C speed), and using `float32` for ML (half the memory of `float64`, sufficient precision for training).

## Pandas — The Data Wrangling Layer

`df[col]` → Series, `df[[cols]]` → DataFrame, `df.describe()` for a quick stats summary, `df.to_csv()`/`pd.read_csv()` for persistence, `df[FEATURES].values` to drop back to a NumPy array for sklearn/PyTorch consumption.

## sklearn — The Universal ML Interface

Every algorithm follows the same three-step shape: `model = SomeAlgorithm()` → `model.fit(X_train, y_train)` → `model.predict(X)`.

- `train_test_split` **before** fitting — fitting on the full dataset makes every downstream metric a lie.
- `StandardScaler` (mean=0, std=1) is required for linear models and neural nets; tree-based models (RF, XGBoost) don't need it.
- `mean_absolute_error` — interpretable, same units as the target ("off by X berries on average").
- `r2_score` — 1.0 perfect, 0.0 no better than predicting the mean, negative worse than the mean.
- **XGBoost** — gradient boosting, trees built sequentially, each correcting the last one's errors. Often the strongest classical model on tabular data and a frequent interview topic.
- **Cross-validation** — a single train/test split can be lucky or unlucky; `cross_val_score(model, X, y, cv=5, ...)` averages across K splits for a more reliable estimate.
- **GridSearchCV** — exhaustively tries hyperparameter combinations under cross-validation and returns `best_params_`.

## PyTorch — The Three Things to Know Cold

1. **`nn.Module`** — every model subclasses it and defines `forward()`. `BountyNet` is `nn.Sequential(Linear(5,64), ReLU(), Linear(64,1))`.
2. **Tensors** — like NumPy arrays, but GPU-capable and gradient-tracking.
3. **The training loop** — forward → loss → `zero_grad()` → `backward()` → `step()`. PyTorch *accumulates* gradients by default; skipping `zero_grad()` adds the previous batch's gradients to the new ones and the model learns garbage.

## Model Evaluation

**Regression (Part A):** MAE (interpretable, same units), RMSE (penalizes large errors more), R² (variance explained).

**Classification (Part B):** Accuracy (only reliable on balanced classes), Precision = TP/(TP+FP) (minimize false alarms), Recall = TP/(TP+FN) (minimize missed detections), F1 (balance of both, for imbalanced data), AUC-ROC (threshold-independent discrimination, 0.5 = random).

**Rule of thumb:** false negatives dangerous (missed disease, missed fraud) → optimize Recall. False positives costly (blocked legit users) → optimize Precision. Need both → F1. Comparing models without committing to a threshold → AUC-ROC.

## W&B — Experiment Tracking

`wandb.init(project=..., config={...})` then `wandb.log({...})` inside the loop. Every ML team runs training this way — log from day one, not after something breaks.

## Gradio — Ship a Model in ~10 Lines

`gr.Interface(fn=predict, inputs=[...], outputs="text").launch()` turns any Python function into a shareable web app. This is the same mechanism HuggingFace Spaces demos run on.

---

## Where This Sits in the Roadmap

This project is the first time data (Phase 1 SQL/Python), a served API shape (Phase 2 FastAPI), and an actual trained model come together. The `BountyNet` class is the direct evolution of the method-chaining OOP pattern from `phase-1-devilfruit`'s `DevilFruit` class — both are pipelines built from composable steps, just declarative (`nn.Sequential`) instead of chained method calls.

**Forward references:**
- **Phase 4** — `3-ML/6-ml-tools/01-huggingface-pipeline.py` runs a pre-trained transformer in 3 lines; Phase 4 explains *why* those models work (tokenization, embeddings, attention) — the natural next question after building a model from scratch here.
- **Phase 5** — `BountyNet`'s checkpoint is servable through the exact same FastAPI pattern built in `phase-2-grandlineAPI`: load once via `Depends()`, accept input via a Pydantic schema, return the prediction as JSON.
