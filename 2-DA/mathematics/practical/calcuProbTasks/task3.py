
# TASK 3: GENERATE 1000 SAMPLES AND PLOT HISTOGRAM

import numpy as np
import matplotlib.pyplot as plt

mean = 100
std = 15
samples = np.random.normal(mean, std, 1000)

# Statistics
print("Mean:", np.mean(samples))
print("Variance:", np.var(samples))
print("Std Dev:", np.std(samples))

# Histogram
plt.hist(samples, bins=30, density=True, alpha=0.7, color='skyblue')
plt.axvline(np.mean(samples), color='red', linestyle='dashed', linewidth=2)
plt.title("Normal Distribution Samples")
plt.xlabel("Value")
plt.ylabel("Density")
plt.show()