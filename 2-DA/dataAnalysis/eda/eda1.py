import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns

data = {
    "Name": ["Carl","Anna","John","Mike","Sara","Lily","Tom"],
    "Age": [23,21,25,22,24,22,23],
    "Score": [90,85,88,92,79,95,87],
    "Gender": ["M","F","M","M","F","F","M"]
}

df = pd.DataFrame(data)

# DATASET INFORMATION
print(df.head())       # first 5 rows
print(df.info())       # column info, data types
print(df.describe())   # statistical summary
print(df.isnull().sum())  # check missing values

# SUMMARY OF DATASET
print("Average Score:", df["Score"].mean())
print("Max Score:", df["Score"].max())
print("Min Score:", df["Score"].min())
print("Median Age:", df["Age"].median())

# GROUPING OF DATA
grouped = df.groupby("Gender")["Score"].mean()
print(grouped)

# HISTOGRAM = MATPLOTLIB
plt.hist(df["Score"], bins=5, color='skyblue', edgecolor='black')
print("Average Score:", df["Score"].mean())
print("Max Score:", df["Score"].max())
print("Min Score:", df["Score"].min())
print("Median Age:", df["Age"].median())

# SCATTER PLOT = AGE VS SCORE:
plt.scatter(df["Age"], df["Score"], color='green')
plt.title("Age vs Score")
plt.xlabel("Age")
plt.ylabel("Score")
plt.show()

# BOXPLOT OF SCORES BY GENDER
sns.boxplot(x="Gender", y="Score", data=df)
plt.title("Score Distribution by Gender")
plt.show()

# HEATMAP OF CORRELATION
corr = df.select_dtypes(include="number").corr()
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()

# OUTLIERS
sns.boxplot(df["Score"])
plt.show()