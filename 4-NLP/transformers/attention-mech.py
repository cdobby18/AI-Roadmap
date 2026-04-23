import tensorflow as tf
from tensorflow.keras.layers import Attention, Input
from tensorflow.keras.models import Model

query = Input(shape=(10,64))
value = Input(shape=(10,64))

attention = Attention()([query, value])

model = Model(inputs=[query,value], outputs=attention)

model.summary()