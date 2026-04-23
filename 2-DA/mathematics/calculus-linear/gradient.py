import numpy as np

def gradient(x,y):

    df_dx = 2*x
    df_dy = 2*y

    return np.array([df_dx, df_dy])

print(gradient(3,4))

# GRADIENT DESCENT
x = 8
learning_rate = 0.1

for i in range(10):

    gradient = 2*x

    x = x - learning_rate * gradient

    print("Iteration:", i, "x:", x)