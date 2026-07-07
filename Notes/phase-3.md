# Phase 3 — Machine Learning

## Goal
Understand how to turn data into predictions, choose the right model, evaluate it honestly, and track experiments the way a real ML team does.

## What I need to know
- NumPy arrays and vectorized operations
- Pandas DataFrames and EDA
- Train/test split and feature scaling
- Classical supervised models: linear regression, logistic regression, decision trees, random forest, XGBoost
- Unsupervised learning: k-means clustering, PCA
- Cross-validation and hyperparameter tuning
- Neural networks and PyTorch basics, plus CNNs for images
- Training loop: forward, loss, backward, optimize
- Evaluation metrics: accuracy, precision, recall, F1
- Overfitting, regularization, and the bias-variance tradeoff
- Experiment tracking (Weights & Biases) and quick demos (Gradio)
- Inference helpers like Hugging Face `pipeline`

## Key terms

### Data and features
- `feature`: input variable used by the model — the things you measure about each example (age, text length, pixel values).
- `label`: the true value the model tries to predict, e.g. `spam` or `not spam`.
- `feature scaling`: transforming features to a similar range (e.g. `StandardScaler`) so models like logistic regression, SVMs, or neural nets converge properly and no feature dominates due to scale alone. Tree-based models generally don't need it.
- `train/test split`: separating data into training and validation sets so you evaluate on unseen data rather than memorized answers.

### Classical ML
- `linear regression`: predicts a continuous value as a weighted sum of features. Baseline for regression problems.
- `logistic regression`: predicts a probability for classification using a sigmoid on top of a linear combination. Simple, fast, interpretable baseline for classification.
- `decision tree`: splits data on feature thresholds to reach a prediction. Easy to interpret but prone to overfitting alone.
- `random forest`: an ensemble of many decision trees trained on random subsets of data/features, averaging their votes. Reduces overfitting vs a single tree (bagging).
- `XGBoost / gradient boosting`: builds trees sequentially, each one correcting the errors of the previous ones (boosting). Usually the strongest classical baseline for tabular data.
- `cross-validation (k-fold)`: splitting data into k folds, training on k-1 and validating on the remaining fold, k times. Gives a more reliable performance estimate than a single train/test split, especially on small data.
- `hyperparameter tuning`: searching over model settings (learning rate, tree depth, number of estimators) via grid search or random search to find the best-performing configuration, validated with cross-validation.

### Unsupervised learning
- `k-means clustering`: groups data into k clusters by repeatedly assigning points to the nearest centroid and recomputing centroids. Requires choosing k in advance.
- `elbow method`: plotting inertia (within-cluster variance) against different k values and picking the k where the improvement sharply levels off — a heuristic for choosing k in k-means.
- `PCA (Principal Component Analysis)`: reduces the number of features by projecting data onto the directions (principal components) that capture the most variance. Used for visualization, noise reduction, and speeding up downstream models.

### Deep learning
- `loss`: a score measuring model error; the model tries to lower loss during training, and lowering loss is what guides learning.
- `optimizer`: algorithm that updates weights to reduce loss (SGD, Adam) — controls how fast and how stably the model learns.
- `epoch`: one full pass through the training dataset. More epochs mean more learning, but too many can overfit.
- `tensor`: multi-dimensional array in PyTorch — the fundamental structure for inputs, weights, and gradients.
- `CNN (convolutional neural network)`: a network using convolution layers that slide small filters over an image to detect local patterns (edges, textures), followed by pooling to downsample. Standard architecture for image tasks.
- `pooling`: downsampling a feature map (e.g. max pooling takes the largest value in each region) to reduce size and add translation invariance.
- `dropout`: randomly zeroing out a fraction of neurons during training to prevent co-adaptation and reduce overfitting.
- `regularization (L1/L2)`: adding a penalty on large weights to the loss function to discourage overfitting; L1 can zero out weights entirely (feature selection), L2 shrinks them smoothly.
- `overfitting`: when a model learns noise in the training data and performs worse on new data. Combat it with more data, regularization, dropout, early stopping, or a simpler model.
- `bias-variance tradeoff`: a high-bias model is too simple (underfits); a high-variance model is too sensitive to training data (overfits). Good models balance the two.

### Evaluation
- `accuracy`: fraction of correct predictions — misleading on imbalanced data (e.g. 95% accuracy predicting "not fraud" when fraud is 5% of cases).
- `precision`: of everything predicted positive, how much was actually positive. Matters when false positives are costly.
- `recall`: of everything actually positive, how much was caught. Matters when false negatives are costly (e.g. missing a disease diagnosis).
- `F1 score`: harmonic mean of precision and recall — a single number when you need to balance both.

### Tooling
- `pipeline`: a Hugging Face helper for inference that wraps tokenizer, model, and post-processing into one call.
- `Weights & Biases (wandb)`: experiment tracking tool that logs metrics, hyperparameters, and artifacts across training runs so you can compare experiments instead of guessing which config worked.
- `Gradio`: a library for quickly wrapping a model in a shareable web demo/UI without building a full frontend.

## When to use
- Use this phase when building a model from data.
- Use classical ML for tabular data and quick, interpretable baselines — try logistic regression or random forest before reaching for deep learning.
- Use XGBoost/gradient boosting when you need the strongest tabular performance and can afford tuning.
- Use k-means/PCA when you need to explore structure in unlabeled data or reduce dimensionality before modeling.
- Use cross-validation whenever your dataset is small enough that a single split gives a noisy estimate.
- Use PyTorch when you need a neural network, custom training loop, or the task is images/text/audio (CNNs, transformers).
- Use `wandb` once you're running more than a couple of experiments and need to compare them reliably.
- Use `Gradio` to demo a model to a non-technical stakeholder without building an app.

## Interview review
- Explain why you split data: training to learn, testing to check generalization, cross-validation to reduce variance in that estimate on small data.
- If asked about metrics, describe how precision and recall trade off, and why you'd pick one over accuracy for imbalanced classes (fraud, disease detection, spam).
- Talk about why `model.eval()` and `torch.no_grad()` matter at inference time — they disable dropout/batchnorm training behavior and stop tracking gradients, saving memory.
- Describe a simple model selection process: start with a baseline (logistic regression / mean predictor), compare metrics via cross-validation, then improve with feature engineering or a stronger model (random forest → XGBoost → neural net) only if justified.
- If asked "how do you know your model isn't overfitting," mention comparing train vs validation loss/metrics, and techniques to fix it: more data, regularization, dropout, early stopping, simpler model.
- If asked when to use k-means vs a supervised model, clarify k-means is for when you don't have labels and want to discover structure.
- If asked how you track experiments, mention logging hyperparameters, metrics, and artifacts (e.g. with `wandb`) so results are reproducible and comparable — not just print statements.
- Be ready to explain bagging (random forest, trains in parallel, reduces variance) vs boosting (XGBoost, trains sequentially, reduces bias) — a very common interview question.

## Common pitfalls
- Scaling features after the train/test split using stats from the full dataset — this leaks test data into training. Fit the scaler on train only, then transform test.
- Using accuracy as the only metric on an imbalanced dataset.
- Tuning hyperparameters against the test set instead of a separate validation set or cross-validation — this quietly overfits to the test set.
- Forgetting `model.eval()` / `torch.no_grad()` at inference, wasting memory and getting inconsistent outputs from dropout.
- Picking k in k-means arbitrarily instead of using the elbow method or a domain-driven choice.
- Jumping straight to deep learning on small tabular data where a tuned XGBoost model would perform as well or better with far less compute.

## How to use

### Data loading
```python
import pandas as pd

df = pd.read_csv("data.csv")
print(df.head())
```

### Train/test split and scaling
```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # transform only, never fit on test
```

### Classical model
```python
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train, y_train)
preds = model.predict(X_test)
```

### Random forest and XGBoost
```python
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

rf = RandomForestClassifier(n_estimators=200, random_state=42).fit(X_train, y_train)
xgb = XGBClassifier(n_estimators=200, learning_rate=0.1).fit(X_train, y_train)
```

### Cross-validation and hyperparameter tuning
```python
from sklearn.model_selection import GridSearchCV

params = {"max_depth": [3, 5, 7], "n_estimators": [100, 200]}
grid = GridSearchCV(RandomForestClassifier(), params, cv=5, scoring="f1")
grid.fit(X_train, y_train)
print(grid.best_params_)
```

### K-means and PCA
```python
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

kmeans = KMeans(n_clusters=3, random_state=42).fit(X)
clusters = kmeans.labels_

pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)
```

### PyTorch training loop
```python
import torch
from torch import nn

model = nn.Linear(input_dim, 1)
criterion = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

for epoch in range(10):
    optimizer.zero_grad()
    outputs = model(X_train)
    loss = criterion(outputs.squeeze(), y_train)
    loss.backward()
    optimizer.step()

model.eval()
with torch.no_grad():
    test_outputs = model(X_test)
```

### Simple CNN
```python
import torch.nn as nn

class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2)
        self.fc = nn.Linear(16 * 14 * 14, 10)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = x.view(x.size(0), -1)
        return self.fc(x)
```

### Evaluation
```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
print(accuracy_score(y_test, preds))
print(precision_score(y_test, preds))
print(recall_score(y_test, preds))
print(f1_score(y_test, preds))
```

### Hugging Face pipeline
```python
from transformers import pipeline
sentiment = pipeline("sentiment-analysis")
print(sentiment("AI engineering notes are useful."))
```

### Experiment tracking with wandb
```python
import wandb

wandb.init(project="ai-roadmap", config={"lr": 1e-3, "epochs": 10})
for epoch in range(10):
    wandb.log({"epoch": epoch, "loss": loss.item()})
```

### Quick demo with Gradio
```python
import gradio as gr

def predict(text):
    return sentiment(text)[0]["label"]

gr.Interface(fn=predict, inputs="text", outputs="text").launch()
```
