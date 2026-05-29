import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

X = np.array([
    [25, 50000], [35, 65000], [45, 80000],
    [20, 20000], [30, 40000], [50, 90000],
])
y = np.array([0, 1, 1, 0, 0, 1])

model = RandomForestClassifier()

param_grid = {
    "n_estimators": [10, 50, 100],
    "max_depth": [2, 4, 6],
}

grid = GridSearchCV(model, param_grid, cv=3)
grid.fit(X, y)

print("Best parameters:", grid.best_params_)
print("Best score:", grid.best_score_)
