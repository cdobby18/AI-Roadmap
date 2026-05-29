import numpy as np

arr = np.array([10, 20, 30, 40, 50])

# Indexing
print(arr[0])   # 10
print(arr[-1])  # 50

# Slicing
print(arr[1:4])   # [20 30 40]
print(arr[:3])    # [10 20 30]
print(arr[::2])   # [10 30 50]

# 2D indexing
matrix = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

print(matrix[0, 1])   # 2
print(matrix[1, :])   # [4 5 6] — full second row
print(matrix[:, 0])   # [1 4]   — first column
