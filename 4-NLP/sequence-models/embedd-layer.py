import numpy as np
from tensorflow.keras.layers import Embedding

vocab_size = 10
embedding_dim = 4

embedding = Embedding(vocab_size, embedding_dim)

input_words = np.array([[1,2,3]])

output = embedding(input_words)

print(output)