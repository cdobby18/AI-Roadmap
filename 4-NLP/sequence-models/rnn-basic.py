import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, SimpleRNN, Dense, Input

model = Sequential([
    Input(shape=(10,)),          # define input length
    Embedding(input_dim=1000, output_dim=32),
    SimpleRNN(units=32),
    Dense(units=1, activation="sigmoid")
])

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

model.summary()