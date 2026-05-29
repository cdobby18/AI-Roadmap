"""
SQL LEVEL 4: AGGREGATIONS

Concepts:
- COUNT()
- AVG()
- SUM()
- GROUP BY

Why:
Basic analytics before ML
"""

import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="ai_course"
)

cursor = db.cursor()

# Count users
cursor.execute("SELECT COUNT(*) FROM users")

# Average age
cursor.execute("SELECT AVG(age) FROM users")

# Grouping
cursor.execute("""
SELECT goal, COUNT(*) 
FROM users 
GROUP BY goal
""")

print(cursor.fetchall())