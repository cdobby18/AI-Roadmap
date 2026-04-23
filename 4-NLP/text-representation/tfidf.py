from sklearn.feature_extraction.text import TfidfVectorizer

corpus = [
    "AI is amazing",
    "AI is the future",
    "Machine learning powers AI"
]

vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(corpus)

print(X.toarray())