import nltk
nltk.download('punkt')

from nltk.tokenize import word_tokenize

text = "Natural Language Processing is amazing."

tokens = word_tokenize(text)

print(tokens)