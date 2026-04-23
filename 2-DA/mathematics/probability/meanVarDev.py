import numpy as np

data = np.random.normal(50,10,1000)

mean = np.mean(data)
variance = np.var(data)
std = np.std(data)

print("Mean:",mean)
print("Variance:",variance)
print("Standard deviation:",std)