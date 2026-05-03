
# TASK 5: COMPUTE MEAN - VARIANCE - STANDARD DEV
import numpy as np

data = np.random.randint(1, 101, size=50)  # random integers 1-100

mean = np.mean(data)
variance = np.var(data)
std = np.std(data)

print("Dataset:", data)
print("Mean:", mean)
print("Variance:", variance)
print("Standard Deviation:", std)