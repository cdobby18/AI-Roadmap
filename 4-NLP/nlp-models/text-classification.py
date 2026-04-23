from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

texts = [
    "good product",
    "excellent service",
    "bad experience",
    "terrible support"
]

labels = [1,1,0,0]

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", LogisticRegression())
])

pipeline.fit(texts, labels)

prediction = pipeline.predict(["excellent product"])

print(prediction)