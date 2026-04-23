# Task 13: Save 5 Students' Scores to JSON and Read It

import json

# Sample student scores
students = {
    "Alice": 85,
    "Bob": 90,
    "Charlie": 78,
    "David": 92,
    "Eva": 88
}

# Save to JSON file
with open("students.json", "w") as f:
    json.dump(students, f)

# Read JSON file
with open("students.json", "r") as f:
    data = json.load(f)

print("Student Scores:", data)