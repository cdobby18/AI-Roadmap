import nltk
nltk.download('wordnet')

from nltk.stem import PorterStemmer, WordNetLemmatizer

words = ["running", "runs", "ran", "easily"]

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

stemmed = [stemmer.stem(w) for w in words]
lemmatized = [lemmatizer.lemmatize(w) for w in words]

print("Stemmed:", stemmed)
print("Lemmatized:", lemmatized)