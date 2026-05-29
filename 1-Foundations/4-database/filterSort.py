"""
SQL LEVEL 3: FILTERING & SORTING

Concepts:
- WHERE
- AND / OR
- ORDER BY
- LIMIT

Why:
Used for extracting datasets
"""

import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="ai_course"
)

cursor = db.cursor()

# Filter
cursor.execute("SELECT * FROM users WHERE age > 20")

# Sort
cursor.execute("SELECT * FROM users ORDER BY age DESC")

# Limit
cursor.execute("SELECT * FROM users LIMIT 5")

for row in cursor:
    print(row)