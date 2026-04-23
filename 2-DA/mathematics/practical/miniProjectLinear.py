import numpy as np

# STEP 1 — Create Dataset

X = np.array([1, 2, 3, 4, 5]) # Hours studied (feature)
y = np.array([50, 55, 65, 70, 80]) # Exam scores (target)

# STEP 2 — Convert X to Matrix
# Add bias column (column of 1s for intercept)

X = np.column_stack((np.ones(len(X)), X))
print("Design Matrix X:")
print(X)

# STEP 3 — Apply Linear Regression Formula

beta = np.linalg.inv(X.T @ X) @ X.T @ y

print("\nBeta Coefficients:")
print(beta)

intercept = beta[0]
slope = beta[1]

print("\nIntercept:", intercept)
print("Slope:", slope)

# STEP 4 — Final Regression Equation

print("\nRegression Equation:")
print(f"Score = {intercept:.2f} + {slope:.2f} * Hours")

# STEP 5 — Make Prediction
hours = 6
predicted_score = intercept + slope * hours

print("\nPrediction")
print("Hours studied:", hours)
print("Predicted Score:", predicted_score)

# STEP 6 — Predict for Multiple Hours

hours_test = np.array([6, 7, 8])
predictions = intercept + slope * hours_test

print("\nMultiple Predictions")
for h, p in zip(hours_test, predictions):
    print(f"Hours: {h} -> Predicted Score: {p}")