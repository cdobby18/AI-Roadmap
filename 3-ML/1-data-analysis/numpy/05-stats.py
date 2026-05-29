import numpy as np

arr = np.array([10, 20, 30, 40])

# Aggregations
print("mean:", np.mean(arr))
print("max:", np.max(arr))
print("min:", np.min(arr))
print("sum:", np.sum(arr))
print("std:", np.std(arr))

# Array creation functions
print(np.zeros((3, 3)))
print(np.ones((2, 4)))
print(np.arange(0, 10))       # [0 1 2 ... 9]
print(np.linspace(0, 10, 5))  # [0. 2.5 5. 7.5 10.]

# Random numbers
random_arr = np.random.rand(5)    # uniform [0, 1)
random_ints = np.random.randint(0, 100, size=5)
print(random_arr)
print(random_ints)
