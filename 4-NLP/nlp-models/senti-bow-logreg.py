from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

texts = [
    "I love this movie",
    "This film is amazing",
    "I hate this movie",
    "This film is terrible"
]

labels = [1,1,0,0]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

model = LogisticRegression()
model.fit(X, labels)

test = ["I love this film"]
test_vec = vectorizer.transform(test)

prediction = model.predict(test_vec)

print("Prediction:", prediction)