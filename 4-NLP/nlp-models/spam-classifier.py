from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

emails = [
    "Win money now",
    "Claim your free prize",
    "Meeting tomorrow at office",
    "Project deadline discussion"
]

labels = [1,1,0,0]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(emails)

model = MultinomialNB()
model.fit(X, labels)

test = ["Win a free lottery"]
test_vec = vectorizer.transform(test)

prediction = model.predict(test_vec)

print("Spam Prediction:", prediction)