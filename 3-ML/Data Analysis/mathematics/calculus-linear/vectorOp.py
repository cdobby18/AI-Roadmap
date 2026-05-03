import numpy as np

v1 = np.array([1,2,3])
v2 = np.array([4,5,6])

# ADDITION - SUBTRACTION
print("Addition:", v1 + v2)
print("Subtraction:", v2 - v1)

# MULTIPLICATION
print(2 * v1)  # [2 4 6]

# DOT PRODUCT
print(np.dot(v1, v2))  # 32