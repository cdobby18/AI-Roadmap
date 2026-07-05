# Phase 3 — Machine Learning

## Goal
Understand how to turn data into predictions, evaluate models, and prepare for real AI workflows.

## What I need to know
- NumPy arrays and vectorized operations
- Pandas DataFrames and EDA
- Train/test split and feature scaling
- Classical models: linear regression, logistic regression, decision trees
- Neural networks and PyTorch basics
- Training loop: forward, loss, backward, optimize
- Evaluation metrics: accuracy, precision, recall, F1
- Inference helpers like Hugging Face `pipeline`

## Key terms
- `feature`: input variable used by the model. In interviews, say that features are the things you measure about each example, like age, text length, or pixel values.
- `label`: the true value the model tries to predict. Labels are what you use to teach the model, for example `spam` or `not spam`.
- `train/test split`: separating data into training and validation sets. This is how you avoid memorizing the answers and instead evaluate real performance.
- `loss`: a score that measures model error. The model tries to lower loss during training, and a good interview answer says loss guides learning.
- `optimizer`: algorithm that updates weights to reduce loss. Common ones are SGD and Adam, and they control how fast the model learns.
- `epoch`: one pass through the entire training dataset. More epochs means more learning, but too many can overfit.
- `tensor`: multi-dimensional array in PyTorch. It is the fundamental data structure for inputs, weights, and gradients.
- `pipeline`: a Hugging Face helper for inference. It wraps tokenizer, model, and post-processing into one easy call.
- `overfitting`: when a model learns noise in the training data and performs worse on new data. Interviewers expect you to mention validation and regularization.
- `bias-variance tradeoff`: a core ML concept. A high-bias model is too simple, a high-variance model is too sensitive to training data.

## When to use
- Use this phase when building a model from data.
- Use classical ML for tabular tasks and quick baselines.
- Use PyTorch when you need a neural network or custom training loop.
- Use evaluation metrics to prevent overfitting and compare models.

## Interview review
- Explain why you split data: training to learn, testing to check generalization.
- If asked about metrics, describe how precision and recall matter for imbalanced classes.
- Talk about why `model.eval()` and `torch.no_grad()` are important in inference to prevent dropout and reduce memory.
- Describe a simple model selection process: start with a baseline, compare metrics, then improve with feature engineering.

## How to use

### Data loading
```python
import pandas as pd

df = pd.read_csv("data.csv")
print(df.head())
```

### Train/test split
```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

### Classical model
```python
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train, y_train)
preds = model.predict(X_test)
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
```

### Evaluation
```python
from sklearn.metrics import accuracy_score, precision_score, recall_score
print(accuracy_score(y_test, preds))
print(precision_score(y_test, preds))
print(recall_score(y_test, preds))
```

### Hugging Face pipeline
```python
from transformers import pipeline
sentiment = pipeline("sentiment-analysis")
print(sentiment("AI engineering notes are useful."))
```
