"""
MINI PROJECT - NumPy Student Score Analyzer

Objectives:
- store students scores in numPy array
- calculate:
    - average
    - highest
    - lowest
    - total
"""

import numpy as np

scores = np.array([85,90,92,97,95])

print("Average: ", np.mean(scores))
print("Highest: ", np.max(scores))
print("Lowest: ", np.min(scores))
print("Overall Score: ", np.sum(scores))
