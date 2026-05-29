"""
SQL LEVEL 7: PYTHON + SQL (REAL AI WORKFLOW)

Concepts:
- Load DB → Pandas
- Data processing

Why:
This is how ML pipelines start
"""

import mysql.connector
import pandas as pd

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="ai_course"
)

# Load into DataFrame
df = pd.read_sql("SELECT * FROM users", db)

# Feature engineering
df["age_group"] = df["age"].apply(lambda x: "Adult" if x >= 21 else "Young")

print(df)

db.close()