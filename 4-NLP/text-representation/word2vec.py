from gensim.models import Word2Vec

sentences = [
    ["machine","learning","is","fun"],
    ["deep","learning","is","powerful"],
    ["AI","is","the","future"]
]

model = Word2Vec(sentences, vector_size=50, window=3, min_count=1)

print(model.wv["learning"])