import tensorflow as tf
import numpy as np

X = np.array([
    [1, 2],
    [2, 3],
    [3, 3],
    [6, 5],
    [7, 7],
    [8, 8]
], dtype=np.float32)

y = np.array([0, 0, 0, 1, 1, 2], dtype=np.int32)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(8, activation='relu', input_shape=(2,)),
    tf.keras.layers.Dense(3, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(X, y, epochs=200, verbose=0)

test_input = np.array([[5, 5]], dtype=np.float32)
prediction = model.predict(test_input)

print("Raw probabilities:", prediction)
print("Predicted class:", np.argmax(prediction))