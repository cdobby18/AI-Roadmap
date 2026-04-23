import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

text = "NLP pipelines clean text, tokenize words, and remove noise."

clean = re.sub(r'[^a-zA-Z\s]', '', text).lower()

tokens = word_tokenize(clean)

stop_words = set(stopwords.words('english'))

processed = [w for w in tokens if w not in stop_words]

print(processed)