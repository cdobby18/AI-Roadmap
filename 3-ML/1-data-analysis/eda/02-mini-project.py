"""
Mini Project — Student EDA

Tasks:
- Load dataset (CSV or manual dict)
- Check for missing values and duplicates
- Compute average, median, max, min of scores and age
- Group by gender and compute mean score
- Visualize: histogram, scatter plot, boxplot, correlation heatmap
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = {
    "Name": ["Carl", "Anna", "John", "Mike", "Sara", "Lily", "Tom"],
    "Age": [23, 21, 25, 22, 24, 22, 23],
    "Score": [90, 85, 88, 92, 79, 95, 87],
    "Gender": ["M", "F", "M", "M", "F", "F", "M"]
}

df = pd.DataFrame(data)
# Uncomment to load from file instead:
# df = pd.read_csv("students.csv")

# 1. Missing values and duplicates
print("Missing Values:\n", df.isnull().sum())
print("Duplicate Rows:", df.duplicated().sum())

# 2. Statistics
print("\n--- Statistics ---")
print("Avg Age:", df["Age"].mean(), "| Median:", df["Age"].median())
print("Avg Score:", df["Score"].mean(), "| Median:", df["Score"].median())
print("Max Score:", df["Score"].max(), "| Min:", df["Score"].min())

# 3. Group by gender
print("\n--- Mean Score by Gender ---")
print(df.groupby("Gender")["Score"].mean())

# 4. Visualizations
plt.figure(figsize=(6, 4))
plt.hist(df["Score"], bins=5, color="skyblue", edgecolor="black")
plt.title("Histogram of Scores")
plt.xlabel("Score")
plt.ylabel("Number of Students")
plt.show()

plt.figure(figsize=(6, 4))
plt.scatter(df["Age"], df["Score"], color="green")
plt.title("Age vs Score")
plt.xlabel("Age")
plt.ylabel("Score")
plt.show()

plt.figure(figsize=(6, 4))
sns.boxplot(x="Gender", y="Score", data=df)
plt.title("Score Distribution by Gender")
plt.show()

plt.figure(figsize=(6, 4))
corr = df.select_dtypes(include="number").corr()
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()
