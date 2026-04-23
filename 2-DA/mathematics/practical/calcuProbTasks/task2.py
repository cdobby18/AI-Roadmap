
# TASK 2: IMPLEMENT GRADIENT DESCENT

import numpy as np

# Function f(x) = x^2 + 4x + 4
def f(x):
    return x**2 + 4*x + 4

# Derivative f'(x) = 2x + 4
def df(x):
    return 2*x + 4

# Gradient descent parameters
x = 0       # initial guess
lr = 0.1    # learning rate
iterations = 20

for i in range(iterations):
    grad = df(x)
    x = x - lr * grad
    print(f"Iteration {i+1}: x = {x}, f(x) = {f(x)}")

print("Minimum at x =", x)