"""
SQL LEVEL 5: JOINS

Concepts:
- INNER JOIN
- Relationships between tables

Why:
Real datasets are NOT in one table
"""

import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="ai_course"
)

cursor = db.cursor()

# Example join
cursor.execute("""
SELECT users.name, orders.product
FROM users
INNER JOIN orders
ON users.id = orders.user_id
""")

for row in cursor:
    print(row)