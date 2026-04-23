import numpy as np

coin = np.random.choice(["H","T"],1000)

heads = np.sum(coin == "H")

probability = heads / 1000

print(probability)