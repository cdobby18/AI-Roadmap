import numpy as np

arr = np.array([[1, 2, 3], [4, 5, 6]])

print("ndim:", arr.ndim)    # number of dimensions
print("shape:", arr.shape)  # (rows, cols)
print("size:", arr.size)    # total elements

# Reshape
reshaped = arr.reshape(3, 2)
print("reshaped:\n", reshaped)

# Flatten back to 1D
print("flattened:", arr.flatten())
