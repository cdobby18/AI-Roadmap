# sql_pandas_eda.py

# 1️⃣ Imports
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 2️⃣ Setup database and table
conn = sqlite3.connect("students.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Age INTEGER CHECK(Age >= 0),
    Score INTEGER CHECK(Score >= 0 AND Score <= 100),
    Gender TEXT CHECK(Gender IN ('M','F'))
);
""")

# Insert sample data
cur.executemany("""
INSERT INTO students (Name, Age, Score, Gender)
VALUES (?, ?, ?, ?)
""", [
    ('Carl', 23, 90, 'M'),
    ('Anna', 21, 85, 'F'),
    ('John', 25, 88, 'M'),
    ('Mike', 22, 92, 'M'),
    ('Sara', 24, 79, 'F'),
    ('Lily', 22, 95, 'F'),
    ('Tom', 23, 87, 'M')
])
conn.commit()

# 3️⃣ Query data into Pandas
df = pd.read_sql_query("SELECT * FROM students", conn)

# 4️⃣ Data cleaning
print("Missing Values:\n", df.isnull().sum())
print("Duplicate Rows:\n", df.duplicated().sum())

# 5️⃣ Summary statistics
print("Average Score:", df["Score"].mean())
print("Median Score:", df["Score"].median())
print("Max Score:", df["Score"].max())
print("Min Score:", df["Score"].min())

# 6️⃣ Group by Gender
print(df.groupby("Gender")["Score"].mean())

# 7️⃣ Visualizations

# Histogram
plt.hist(df["Score"], bins=5, color='skyblue', edgecolor='black')
plt.title("Score Distribution")
plt.xlabel("Score")
plt.ylabel("Number of Students")
plt.show()

# Scatter Plot: Age vs Score
plt.scatter(df["Age"], df["Score"], color='green')
plt.title("Age vs Score")
plt.xlabel("Age")
plt.ylabel("Score")
plt.show()

# Boxplot by Gender
sns.boxplot(x="Gender", y="Score", data=df)
plt.title("Score Distribution by Gender")
plt.show()

# Correlation Heatmap
corr = df.select_dtypes(include="number").corr()
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()

# 8️⃣ Save cleaned data
df.to_csv("students_cleaned.csv", index=False)