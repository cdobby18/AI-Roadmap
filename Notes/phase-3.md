# Phase 3 — Machine Learning

## The ML Workflow

1. Define the problem (classification, regression, clustering)
2. Collect and explore data (EDA)
3. Clean, transform, and split data
4. Train a baseline model
5. Iterate: feature engineering → model selection → hyperparameter tuning
6. Evaluate honestly (never on training data)
7. Deploy or document

**The most important step is #4 — always baseline first.** A simple model tells you whether your data has signal before you invest in complex architectures.

## Key Concepts

### Data

**Features:** Inputs to the model. Garbage in, garbage out — feature quality matters more than model choice.

**Labels:** The ground truth the model tries to predict. For classification, labels are categories (spam/not spam). For regression, labels are continuous values (price, temperature).

**Train/test split:** Train set teaches the model; test set measures generalization. NEVER let the test set influence training decisions (feature selection, hyperparameter tuning) — that's data leakage.

**Cross-validation (k-fold):** Split data into k folds, train on k-1, validate on the remaining fold, repeat k times. Gives a more reliable performance estimate than a single split, especially on small data.

**Feature scaling:** Transform features to similar ranges (standardization: mean=0, std=1). Needed for linear models, SVMs, neural networks — gradient descent converges faster when features are on similar scales. Tree-based models don't need it (they split on thresholds, not distances).

**Data leakage:** When information from outside the training set influences the model. Common causes:
- Scaling before splitting (fit on test data)
- Using future data to predict the past (time series)
- Target leakage (a feature that wouldn't be available at prediction time)

### Classical ML

**Linear regression:** Predicts continuous value as weighted sum of features. Baseline for regression. Interpretable coefficients — you can say "a 1-unit increase in X increases prediction by beta."

**Logistic regression:** Predicts probability for classification. Sigmoid on top of linear combination. Simple, fast, interpretable baseline. Linear decision boundary — can't capture complex patterns without feature engineering.

**Decision trees:** Split data on feature thresholds. Easy to visualize and explain. Prone to overfitting alone — depth and min_samples_split control this.

**Random forest (bagging):** Many trees trained on random subsets of data and features, averaging their votes. Reduces overfitting vs single tree. Parallel training (each tree is independent). Strong default choice for tabular data.

**XGBoost / Gradient boosting (boosting):** Trees built sequentially, each correcting the previous one's errors. Usually strongest classical model for tabular data. More sensitive to hyperparameters than random forest. Sequential training can't parallelize across trees.

**Bagging vs Boosting:** Bagging trains in parallel, reduces variance (overfitting). Boosting trains sequentially, reduces bias (underfitting). Bagging is safer with default params; boosting needs tuning but achieves higher accuracy.

### Unsupervised Learning

**K-means clustering:** Groups data into k clusters by iteratively: (1) assign each point to nearest centroid, (2) recompute centroids. Requires choosing k in advance. Use elbow method (inertia vs k) or silhouette score to pick k.

**PCA:** Reduces feature dimensions by projecting onto directions of maximum variance. Used for visualization (2D/3D plots), noise reduction, speeding up downstream models, and as a preprocessing step. The components are linear combinations of original features — not interpretable as individual features.

### Deep Learning

**Neural network:** Layers of neurons, each doing a linear transformation + nonlinear activation. Universal function approximator — given enough parameters, can learn any function. Requires more data and tuning than classical models.

**Loss function:** Measures prediction error. The model trains to minimize this. Regression: MSE (mean squared error). Classification: cross-entropy. The choice of loss function encodes what kind of error matters.

**Optimizer:** Algorithm that updates weights to reduce loss. SGD (simple, needs learning rate tuning), Adam (adaptive learning rates per parameter, less tuning needed, default choice).

**Backpropagation:** Chain rule applied across the computational graph. Computes gradient of loss with respect to every parameter. Then the optimizer takes a step in the negative gradient direction.

**Epoch:** One full pass through the training data. More epochs = more learning, but too many = overfitting.

**Overfitting:** Model learns noise in training data, performs worse on new data. Signs: training loss keeps decreasing, validation loss starts increasing. Fixes: more data, regularization, dropout, early stopping, simpler model.

**Underfitting:** Model is too simple to capture the pattern. Training loss is high. Fixes: more complex model, more features, train longer.

**Bias-variance tradeoff:** High bias = underfitting (too simple). High variance = overfitting (too sensitive to training data). Goal: balance both.

**CNN:** Uses convolution filters that slide over the input, detecting local patterns (edges, textures). Pooling downsamples to add translation invariance. Standard architecture for images.

**Dropout:** Randomly zeros out neurons during training. Forces the network to not rely on any single neuron — acts as regularization.

**Regularization (L1/L2):** Penalty on large weights added to the loss. L1 (lasso) can zero out weights — feature selection. L2 (ridge) shrinks weights smoothly — prevents any one feature from dominating.

### Evaluation

**Accuracy:** Fraction correct. Misleading on imbalanced data — 95% accuracy detecting fraud is worthless if fraud is 5% of cases (predicting "not fraud" every time gives 95%).

**Precision:** Of things predicted positive, how many were actually positive. High precision = few false positives. Matters when false positives are costly (spam filtering — flagging legitimate email as spam).

**Recall:** Of actual positives, how many were caught. High recall = few false negatives. Matters when false negatives are costly (disease screening — missing a patient).

**F1 score:** Harmonic mean of precision and recall. Single number when you need to balance both.

**ROC-AUC:** Area under the ROC curve (TPR vs FPR at various thresholds). Measures ranking quality — how well the model separates positives from negatives. 0.5 = random, 1.0 = perfect. Use when you care about ranking, not just thresholded predictions.

### Tooling

**HuggingFace pipeline:** Wraps tokenizer + model + post-processing into one call. Use for quick inference with any transformer model. Not for fine-tuning or custom training.

**Weights & Biases (wandb):** Experiment tracking. Logs hyperparameters, metrics, and artifacts per run. Essential once you run more than a few experiments — without it, you can't compare results reliably.

**Gradio:** Quick web demo for any model. Wrap any predict function in a UI in 3 lines. Use for stakeholder demos, not production.

## When to Use What

| Scenario | Start with |
|---|---|
| Tabular data, need quick baseline | Logistic regression or random forest |
| Tabular data, want best accuracy | XGBoost (after tuning) |
| Images | CNN / ResNet / ViT |
| Text | Transformer (BERT for understanding, GPT for generation) |
| Small data, need interpretability | Decision tree or logistic regression |
| No labels, want to find structure | K-means or PCA |
| Very large dataset | Start with a sample, iterate, then scale |

**Rule of thumb:** Always beat a simple baseline (mean predictor, most-frequent-class) before trying complex models. Most of your performance gains come from data quality and feature engineering, not model choice.

## Interview Must-Knows

- Why split data: train to learn, test to measure generalization. Cross-validation for more reliable estimates on small data.
- Why scale features: gradient descent converges faster. Tree models don't need it.
- Overfitting vs underfitting: signs, causes, fixes for each.
- Bagging vs boosting: bagging reduces variance (parallel trees, random forest), boosting reduces bias (sequential trees, XGBoost).
- Precision vs recall: which matters depends on cost of false positives vs false negatives.
- When deep learning is overkill: small tabular data where XGBoost matches or outperforms.
- Data leakage examples and how to avoid them.
- `model.eval()` + `torch.no_grad()` at inference: disables dropout/batchnorm training behavior, stops gradient tracking (saves memory).

## Common Pitfalls

- Scaling before train/test split (leaks test data into training)
- Using accuracy on imbalanced data
- Tuning hyperparameters on the test set (overfits to test)
- Forgetting model.eval() / torch.no_grad() at inference
- Jumping to deep learning on small tabular data where XGBoost works better
- Not baselining — can't know if your complex model is actually better than simple
