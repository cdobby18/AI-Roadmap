from sklearn.model_selection import cross_val_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

texts = [
    "good product",
    "excellent support",
    "bad service",
    "terrible experience"
]

labels = [1,1,0,0]

vectorizer = CountVectorizer()

X = vectorizer.fit_transform(texts)

model = LogisticRegression()

scores = cross_val_score(model, X, labels, cv=2)

print(scores)