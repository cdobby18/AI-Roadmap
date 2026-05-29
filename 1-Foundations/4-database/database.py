"""
SQL LEVEL 1: DATABASE & TABLE CREATION (DDL)

Concepts:
- CREATE DATABASE
- CREATE TABLE
- Data types
- Primary Key

Why:
This defines your DATA STRUCTURE (schema)
"""

import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password"
)

cursor = db.cursor()

# Create database
cursor.execute("CREATE DATABASE IF NOT EXISTS ai_course")

# Select database
cursor.execute("USE ai_course")

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,   -- Unique identifier
    name VARCHAR(100),                  -- Text
    age INT,                            -- Number
    goal VARCHAR(255)                   -- Text
)
""")

print("✅ Database and table ready")