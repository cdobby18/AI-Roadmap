# Phase 3 · Machine Learning

This phase takes you from raw data to trained models, deep learning fundamentals, and the tools used in real AI engineering workflows.

**Prerequisite:** Phase 1 (Foundations) + Phase 2 (FastAPI)  
**Next:** Phase 4 (NLP)

---

## Structure

| Folder | Topic | Status |
|--------|-------|--------|
| `1-data-analysis/` | NumPy, Pandas, EDA, SQL | |
| `2-classical-ml/` | Supervised + Unsupervised Learning | |
| `3-deep-learning/` | Neural Networks, CNN (TensorFlow) | |
| `4-pytorch/` | Tensors, nn.Module, Training Loop | |
| `5-model-evaluation/` | Metrics, Confusion Matrix | |
| `6-ml-tools/` | Hugging Face, W&B, Gradio | |

---

## Master Progress Checklist

### 1 · Data Analysis
- [ ] NumPy: arrays, dimensions, indexing, vector ops, stats
- [ ] Pandas: Series, DataFrame, read CSV, mini project
- [ ] EDA: 7-step process, visualizations
- [ ] SQL + Pandas: SQLite → DataFrame pipeline

### 2 · Classical ML — Supervised
- [ ] Linear Regression (sklearn + from scratch)
- [ ] Train/test split + feature scaling
- [ ] Binary Classification (Logistic Regression)
- [ ] Decision Tree
- [ ] Random Forest
- [ ] SVM
- [ ] XGBoost
- [ ] Cross-Validation
- [ ] Hyperparameter Tuning (GridSearchCV)

### 2 · Classical ML — Unsupervised
- [ ] K-Means + Elbow Method
- [ ] DBSCAN
- [ ] Hierarchical Clustering + Dendrogram
- [ ] PCA
- [ ] Anomaly Detection (IsolationForest)

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

Study the sections in order — each builds on the previous.

```
1-data-analysis → 2-classical-ml → 3-deep-learning
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
