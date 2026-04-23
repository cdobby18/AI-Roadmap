import nltk
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

text = "This is an example showing stopword removal."

tokens = word_tokenize(text)

stop_words = set(stopwords.words('english'))

filtered = [w for w in tokens if w.lower() not in stop_words]

print(filtered)