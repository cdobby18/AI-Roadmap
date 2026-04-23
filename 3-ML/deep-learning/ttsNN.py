import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

X = np.array([[1], [2], [3], [4], [5], [6], [7], [8]], dtype=np.float32)
y = np.array([0, 0, 0, 0, 1, 1, 1, 1], dtype=np.float32)

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(8, activation='relu', input_shape=(1,)),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

model.fit(X_train, y_train, epochs=200, verbose=0)

loss, acc = model.evaluate(X_test, y_test, verbose=0)
print("Test Loss:", loss)
print("Test Accuracy:", acc)