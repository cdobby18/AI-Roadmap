"""
SQL LEVEL 2: CRUD OPERATIONS

Concepts:
- INSERT
- SELECT
- UPDATE
- DELETE

Why:
This is 90% of backend + AI data pipelines
"""

import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="ai_course"
)

cursor = db.cursor()

# CREATE (Insert)
cursor.execute(
    "INSERT INTO users (name, age, goal) VALUES (%s, %s, %s)",
    ("CJ", 21, "AI Engineer")
)

db.commit()

# READ
cursor.execute("SELECT * FROM users")
print(cursor.fetchall())

# UPDATE
cursor.execute("UPDATE users SET age = 22 WHERE name = 'CJ'")
db.commit()

# DELETE
cursor.execute("DELETE FROM users WHERE name = 'CJ'")
db.commit()