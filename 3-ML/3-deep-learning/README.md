# 3 · Deep Learning

Neural networks are the foundation of modern AI. This section uses TensorFlow/Keras to build and train them before transitioning to PyTorch.

---

## What You'll Learn

- Feature scaling — why it's mandatory before neural nets
- Dense layers — the building block of every network
- Activation functions — ReLU, sigmoid, softmax
- Loss functions and optimizers
- Convolutional Neural Networks (CNNs) for image data

---

## Progress Checklist

- [ ] `01-feature-scaling.py` — StandardScaler before any NN input
- [ ] `02-basic-nn.py` — binary classification with a 2-layer network
- [ ] `03-multi-layer-nn.py` — multi-class classification (3 output classes)
- [ ] `04-cnn.py` — Conv2D + MaxPooling architecture for images

---

## Key Concepts

| Concept | One-liner |
|---------|-----------|
| `Dense` layer | Fully connected — every input connects to every neuron |
| `ReLU` | Default hidden activation — fast, avoids vanishing gradients |
| `sigmoid` | Output layer for binary classification — squashes to [0,1] |
| `softmax` | Output layer for multi-class — probabilities that sum to 1 |
| `binary_crossentropy` | Loss for binary classification |
| `sparse_categorical_crossentropy` | Loss for multi-class with integer labels |
| `adam` | Default optimizer — adaptive learning rate, usually works well |
| `Conv2D` | Learns spatial features (edges, textures) in images |
| `MaxPooling2D` | Reduces spatial size, keeps dominant features |

---

## Note

These files use TensorFlow/Keras. The next section (4-pytorch) covers the same concepts using PyTorch — the industry-standard for research and LLM work.
