import numpy as np

arr = np.array([1, 2, 3, 4])

# Vectorized operations — no Python loops needed
print(arr * 2)    # [2 4 6 8]
print(arr + 5)    # [6 7 8 9]
print(arr ** 2)   # [1 4 9 16]

# Broadcasting: scalar applied to all elements
print(arr > 2)    # [False False  True  True]

# Dot product
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print("dot product:", np.dot(a, b))   # 32
