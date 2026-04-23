import tensorflow as tf
from tensorflow.keras.layers import MultiHeadAttention

attention = MultiHeadAttention(num_heads=4, key_dim=64)

import numpy as np

query = np.random.rand(1,10,64)
value = np.random.rand(1,10,64)

output = attention(query,value)

print(output.shape)