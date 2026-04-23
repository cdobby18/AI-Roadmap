import tensorflow as tf
import numpy as np

X = np.array([[1], [2], [3], [4], [5], [6]], dtype=np.float32)
y = np.array([0, 0, 0, 1, 1, 1], dtype=np.float32)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(4, activation='relu', input_shape=(1,)),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

model.fit(X, y, epochs=200, verbose=0)

test_input = np.array([[3.5]], dtype=np.float32)
prediction = model.predict(test_input)

print("Raw prediction (probability):", prediction)
print("Class (0 or 1):", (prediction > 0.5).astype(int))