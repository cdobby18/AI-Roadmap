# 2 · Classical ML

The algorithms here power most production ML systems. Understand when to use each one and how to evaluate it properly.

---

## What You'll Learn

- **Supervised Learning** — predict a target from labeled data
- **Unsupervised Learning** — find structure in unlabeled data
- **scikit-learn pipeline** — preprocessing → fit → evaluate

---

## Progress Checklist

### Supervised Learning
- [ ] `supervised/01-linear-regression.py` — predict continuous value with sklearn
- [ ] `supervised/02-gradient-descent.py` — build linear regression from scratch
- [ ] `supervised/03-multiple-linear-regression.py` — multiple features + metrics (MAE, MSE, R2)
- [ ] `supervised/04-train-test-split.py` — split data + feature scaling
- [ ] `supervised/05-binary-classification.py` — logistic regression (pass/fail)
- [ ] `supervised/06-decision-tree.py` — tree-based classification
- [ ] `supervised/07-random-forest.py` — ensemble of trees
- [ ] `supervised/08-svm.py` — support vector machine
- [ ] `supervised/09-xgboost.py` — gradient boosting (often wins Kaggle)
- [ ] `supervised/10-cross-validation.py` — more reliable than a single train/test split
- [ ] `supervised/11-hyperparameter-tuning.py` — GridSearchCV

### Unsupervised Learning
- [ ] `unsupervised/01-kmeans.py` — cluster data into k groups
- [ ] `unsupervised/02-elbow-method.py` — find optimal k visually
- [ ] `unsupervised/03-dbscan.py` — density-based clusters + noise detection
- [ ] `unsupervised/04-hierarchical-clustering.py` — agglomerative clustering
- [ ] `unsupervised/05-dendrogram.py` — visualize cluster hierarchy
- [ ] `unsupervised/06-pca.py` — reduce dimensions, preserve variance
- [ ] `unsupervised/07-anomaly-detection.py` — IsolationForest

---

## Key Concepts

| Concept | One-liner |
|---------|-----------|
| `fit` / `predict` | sklearn's universal interface — learn it once, use everywhere |
| `train_test_split` | Never evaluate on data the model has seen |
| `StandardScaler` | Always scale features before SVM, logistic regression, NN |
| Overfitting | Good train score, bad test score — use cross-validation to detect |
| `GridSearchCV` | Exhaustive search over parameter combinations |
| PCA | Compress features — useful when you have hundreds of columns |

---

## Algorithm Cheat Sheet

| Task | Try First | Try If That Fails |
|------|-----------|-------------------|
| Regression | LinearRegression | RandomForest, XGBoost |
| Classification | LogisticRegression | RandomForest, XGBoost, SVM |
| Clustering | KMeans | DBSCAN (handles noise) |
| Dimensionality reduction | PCA | UMAP |
| Anomaly detection | IsolationForest | DBSCAN |
