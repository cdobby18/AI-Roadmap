"""
Demonstrates train/test split and feature scaling — two steps
that should always happen before fitting a model.
"""
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

X = np.array([
    [50, 1],
    [80, 2],
    [100, 3],
    [120, 3],
    [150, 4],
])
y = np.array([100000, 160000, 180000, 220000, 300000])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)   # transform only — never fit on test data

model = LinearRegression()
model.fit(X_train_scaled, y_train)

predictions = model.predict(X_test_scaled)
print("Predicted:", predictions)
