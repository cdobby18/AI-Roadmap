import tensorflow as tf
import numpy as np

# Synthetic image data: 100 samples of 64x64 RGB images, 2 classes
X = np.random.rand(100, 64, 64, 3).astype(np.float32)
y = tf.keras.utils.to_categorical(np.random.randint(0, 2, 100), num_classes=2)

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=(64, 64, 3)),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

    tf.keras.layers.Conv2D(64, (3, 3), activation="relu"),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dense(2, activation="softmax"),
])

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"],
)

model.summary()

model.fit(X, y, epochs=3, batch_size=16, validation_split=0.2, verbose=1)

# Predict on a single synthetic image
sample = np.random.rand(1, 64, 64, 3).astype(np.float32)
prediction = model.predict(sample)
print("Predicted class:", np.argmax(prediction))
