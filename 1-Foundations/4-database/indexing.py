"""
SQL LEVEL 6: INDEXING

Concepts:
- INDEX
- Query optimization

Why:
Critical for large datasets (AI scale)
"""

import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="ai_course"
)

cursor = db.cursor()

# Create index
cursor.execute("CREATE INDEX idx_name ON users(name)")

print("✅ Index created")