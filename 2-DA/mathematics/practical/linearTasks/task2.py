
# TASK 2: MATRIX OPERATIONS

import numpy as np

A = np.array([
    [1,2,3],
    [4,5,6]
])

# SHAPE - TRANSPOSE
print(A)
print(A.shape)
print(A.T)

# MATRIX MULTIPLICATION
B = np.array([[1,2],[3,4]])
C = np.array([[5,6],[7,8]])
print(B @ C)

# IDENTITY
I = np.eye(3)
print(I)

# INVERSE
A = np.array([[4,7],[2,6]])
inv = np.linalg.inv(A)
print(inv)