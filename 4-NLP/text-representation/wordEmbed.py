import tensorflow as tf
import numpy as np

vocab_size = 10
embedding_dim = 4

embedding_layer = tf.keras.layers.Embedding(vocab_size, embedding_dim)

input_data = np.array([[1,2,3]])

output = embedding_layer(input_data)

print(output)