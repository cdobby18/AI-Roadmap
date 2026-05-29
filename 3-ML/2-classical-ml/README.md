# 2 · Classical ML

The supervised algorithms here are foundational — you'll encounter them in interviews and use them when LLMs aren't the right tool. Unsupervised is background context for AI engineers; skim it, don't deep-dive.

---

## Progress Checklist

### Supervised Learning — Required
- [ ] `supervised/01-linear-regression.py` — predict continuous value with sklearn
- [ ] `supervised/02-gradient-descent.py` — build linear regression from scratch
- [ ] `supervised/04-train-test-split.py` — split data + feature scaling
- [ ] `supervised/05-binary-classification.py` — logistic regression (pass/fail)
- [ ] `supervised/06-decision-tree.py` — tree-based classification
- [ ] `supervised/07-random-forest.py` — ensemble of trees
- [ ] `supervised/09-xgboost.py` — gradient boosting (often wins Kaggle)
- [ ] `supervised/10-cross-validation.py` — more reliable than a single train/test split
- [ ] `supervised/11-hyperparameter-tuning.py` — GridSearchCV

### Unsupervised Learning — Optional (skim for context)
- [ ] `unsupervised/01-kmeans.py` — cluster data into k groups
- [ ] `unsupervised/02-elbow-method.py` — find optimal k visually
- [ ] `unsupervised/06-pca.py` — reduce dimensions, preserve variance

---

## Key Concepts

| Concept | One-liner |
|---------|-----------|
| `fit` / `predict` | sklearn's universal interface — learn it once, use everywhere |
| `train_test_split` | Never evaluate on data the model has seen |
| `StandardScaler` | Always scale features before logistic regression, NN |
| Overfitting | Good train score, bad test score — use cross-validation to detect |
| `GridSearchCV` | Exhaustive search over parameter combinations |
| PCA | Compress features — also used in embedding analysis |

---

## Algorithm Cheat Sheet

| Task | Try First | Try If That Fails |
|------|-----------|-------------------|
| Regression | LinearRegression | RandomForest, XGBoost |
| Classification | LogisticRegression | RandomForest, XGBoost |
| Clustering | KMeans | — |
| Dimensionality reduction | PCA | UMAP |
