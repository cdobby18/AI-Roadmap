from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

texts = [
    "AI is amazing",
    "Machine learning is powerful",
    "I dislike bugs",
    "Errors are annoying"
]

labels = [1,1,0,0]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

model = MultinomialNB()
model.fit(X, labels)

test = ["AI is powerful"]
test_vec = vectorizer.transform(test)

print(model.predict(test_vec))