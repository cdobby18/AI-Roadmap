"""
MINI PROJECT - STUDENT EDA

Tasks:
- Load a dataset of students (CSV or manual dictionary).
- Check for missing values and duplicates.
- Compute average, median, max, min of scores and age.
- Group by gender and compute mean score.

Visualize:
    - Histogram of scores
    - Scatter plot: Age vs Score
    - Boxplot by Gender
    - Correlation heatmap

"""

# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load dataset (manual dictionary example)
data = {
    "Name": ["Carl","Anna","John","Mike","Sara","Lily","Tom"],
    "Age": [23,21,25,22,24,22,23],
    "Score": [90,85,88,92,79,95,87],
    "Gender": ["M","F","M","M","F","F","M"]
}

df = pd.DataFrame(data)
df = pd.read_csv("students.csv")

# 2. Check for missing values and duplicates
print("Missing Values:\n", df.isnull().sum())
print("\nDuplicate Rows:\n", df.duplicated().sum())

# 3. Compute statistics
print("\n--- Statistics ---")
print("Average Age:", df["Age"].mean())
print("Median Age:", df["Age"].median())
print("Max Age:", df["Age"].max())
print("Min Age:", df["Age"].min())

print("\nAverage Score:", df["Score"].mean())
print("Median Score:", df["Score"].median())
print("Max Score:", df["Score"].max())
print("Min Score:", df["Score"].min())

# 4. Group by Gender and compute mean Score
print("\n--- Average Score by Gender ---")
gender_group = df.groupby("Gender")["Score"].mean()
print(gender_group)

# 5. Visualizations

# Histogram of Scores
plt.figure(figsize=(6,4))
plt.hist(df["Score"], bins=5, color='skyblue', edgecolor='black')
plt.title("Histogram of Scores")
plt.xlabel("Score")
plt.ylabel("Number of Students")
plt.show()

# Scatter Plot: Age vs Score
plt.figure(figsize=(6,4))
plt.scatter(df["Age"], df["Score"], color='green')
plt.title("Age vs Score")
plt.xlabel("Age")
plt.ylabel("Score")
plt.show()

# Boxplot: Score by Gender
plt.figure(figsize=(6,4))
sns.boxplot(x="Gender", y="Score", data=df)
plt.title("Score Distribution by Gender")
plt.show()

# Correlation Heatmap (numeric columns only)
plt.figure(figsize=(6,4))
corr = df.select_dtypes(include="number").corr()
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()