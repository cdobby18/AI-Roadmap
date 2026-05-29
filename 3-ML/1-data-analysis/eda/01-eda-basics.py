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

# Step 1 — inspect structure
print(df.head())
print(df.info())
print(df.describe())
print("Missing values:\n", df.isnull().sum())

# Step 2 — summary statistics
print("Average Score:", df["Score"].mean())
print("Max Score:", df["Score"].max())
print("Min Score:", df["Score"].min())
print("Median Age:", df["Age"].median())

# Step 3 — grouping
print(df.groupby("Gender")["Score"].mean())

# Step 4 — visualizations
plt.hist(df["Score"], bins=5, color="skyblue", edgecolor="black")
plt.title("Score Distribution")
plt.xlabel("Score")
plt.ylabel("Count")
plt.show()

plt.scatter(df["Age"], df["Score"], color="green")
plt.title("Age vs Score")
plt.xlabel("Age")
plt.ylabel("Score")
plt.show()

sns.boxplot(x="Gender", y="Score", data=df)
plt.title("Score Distribution by Gender")
plt.show()

corr = df.select_dtypes(include="number").corr()
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()
