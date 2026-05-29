import pandas as pd

# Series: 1D labeled array
data = pd.Series([10, 20, 30, 40])
print(data)

# With custom index
scores = pd.Series([90, 85, 92], index=["Carl", "Anna", "John"])
print(scores)
print(scores["Carl"])   # access by label
print(scores[0])        # access by position
print(scores.mean())
