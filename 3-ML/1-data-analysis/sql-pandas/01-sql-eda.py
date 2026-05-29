import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect and create table
conn = sqlite3.connect("students.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Age INTEGER CHECK(Age >= 0),
    Score INTEGER CHECK(Score >= 0 AND Score <= 100),
    Gender TEXT CHECK(Gender IN ('M', 'F'))
)
""")

cur.executemany("""
INSERT INTO students (Name, Age, Score, Gender) VALUES (?, ?, ?, ?)
""", [
    ("Carl", 23, 90, "M"),
    ("Anna", 21, 85, "F"),
    ("John", 25, 88, "M"),
    ("Mike", 22, 92, "M"),
    ("Sara", 24, 79, "F"),
    ("Lily", 22, 95, "F"),
    ("Tom", 23, 87, "M"),
])
conn.commit()

# Load SQL query into DataFrame
df = pd.read_sql_query("SELECT * FROM students", conn)

# Data quality check
print("Missing Values:\n", df.isnull().sum())
print("Duplicate Rows:", df.duplicated().sum())

# Summary statistics
print("Average Score:", df["Score"].mean())
print("Median Score:", df["Score"].median())
print("Max Score:", df["Score"].max())
print("Min Score:", df["Score"].min())
print(df.groupby("Gender")["Score"].mean())

# Visualizations
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

# Save cleaned data
df.to_csv("students_cleaned.csv", index=False)
conn.close()
