
# TASK 4: SIMULATE 1000 COIN FLIPS AND GET PROBABILITY

import numpy as np

# 0 = tails, 1 = heads
flips = np.random.choice([0,1], size=1000)
p_heads = np.mean(flips)
p_tails = 1 - p_heads

print("Estimated probability of heads:", p_heads)
print("Estimated probability of tails:", p_tails)