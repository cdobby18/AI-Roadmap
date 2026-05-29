from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
import numpy as np

X = np.array([
    [1],[2],[3],[4],[5],[6],[7],[8]
])

y = np.array([0,0,0,1,1,1,1,1])

model = LogisticRegression()

scores = cross_val_score(model,X,y,cv=5)

print("Cross validation scores:",scores)
print("Average score:",scores.mean())