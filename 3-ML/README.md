# Phase 3 · Machine Learning

This phase takes you from raw data to trained models, deep learning fundamentals, and the tools used in real AI engineering workflows.

**Prerequisite:** Phase 1 (Foundations) + Phase 2 (FastAPI)  
**Next:** Phase 4 (NLP + Transformers)

---

## Structure

| Folder | Topic | Priority |
|--------|-------|----------|
| `1-data-analysis/` | NumPy, Pandas, EDA, SQL | Required |
| `2-classical-ml/` | Supervised Learning (+ optional unsupervised) | Required (supervised only) |
| `3-deep-learning/` | Neural Networks, CNN (TensorFlow) | Required |
| `4-pytorch/` | Tensors, nn.Module, Training Loop | Required |
| `5-model-evaluation/` | Metrics, Confusion Matrix | Required |
| `6-ml-tools/` | Hugging Face, W&B, Gradio | Required |

---

## What AI Engineers Actually Need Here

Sections 1, 3, 4, 5, and 6 are fully required. For classical ML (section 2), supervised learning is essential — unsupervised is background context, not a daily skill for AI engineers. Skip DBSCAN, hierarchical clustering, and dendrograms; they belong in data science, not AI engineering.

---

## Master Progress Checklist

### 1 · Data Analysis
- [ ] NumPy: arrays, dimensions, indexing, vector ops, stats
- [ ] Pandas: Series, DataFrame, read CSV, mini project
- [ ] EDA: 7-step process, visualizations
- [ ] SQL + Pandas: SQLite → DataFrame pipeline

### 2 · Classical ML — Supervised (Required)
- [ ] Linear Regression (sklearn + from scratch)
- [ ] Train/test split + feature scaling
- [ ] Binary Classification (Logistic Regression)
- [ ] Decision Tree
- [ ] Random Forest
- [ ] XGBoost
- [ ] Cross-Validation
- [ ] Hyperparameter Tuning (GridSearchCV)

### 2 · Classical ML — Unsupervised (Optional — skim, don't deep-dive)
- [ ] K-Means + Elbow Method
- [ ] PCA

### 3 · Deep Learning
- [ ] Feature Scaling
- [ ] Basic Neural Network (binary classification)
- [ ] Multi-Layer NN (multi-class classification)
- [ ] CNN (image classification)

### 4 · PyTorch
- [ ] Tensors
- [ ] nn.Module (custom model class)
- [ ] Training Loop (forward → loss → backward → step)

### 5 · Model Evaluation
- [ ] Accuracy, Precision, Recall, F1, AUC-ROC
- [ ] Confusion Matrix + classification_report

### 6 · ML Tools
- [ ] Hugging Face pipeline() — sentiment, generation, zero-shot
- [ ] W&B — log metrics, compare runs
- [ ] Gradio — deploy a model as a web UI

---

## Learning Path

```
1-data-analysis → 2-classical-ml (supervised) → 3-deep-learning
                                                        ↓
                      6-ml-tools ← 5-model-evaluation ← 4-pytorch
```

---

## Resources

| Resource | What | Format | Cost |
|----------|------|--------|------|
| Kaggle — Pandas course | Best Pandas intro | Interactive | Free |
| NumPy official quickstart | Fast and dense | Docs | Free |
| fast.ai — Practical Deep Learning | Best practical ML course | Video + Notebooks | Free |
| PyTorch official tutorials | Tensors through training loops | Docs + Code | Free |
| Sentdex — PyTorch playlist | Beginner-friendly, builds up | Video | Free |
| Weights & Biases quickstart | Set up W&B in 5 minutes | Docs | Free |
| Gradio docs (gradio.app) | Quickstart only | Docs | Free |
| Hugging Face — Pipeline tutorial | Pre-trained models in one call | Docs | Free |

---

## Capstone Project

**[BountyHunter](../8-Projects/phase-3-bountyhunter/)** — Predict a pirate's bounty with a PyTorch model.

Applies every section of Phase 3 end-to-end:
`data.py` (NumPy/Pandas) → `baseline.py` (sklearn) → `model.py` + `train.py` (PyTorch) → `evaluate.py` (metrics) → `app.py` (Gradio)
