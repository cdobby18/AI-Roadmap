# FILE I/O
import csv

"""
# w - write, a - append, r - read, + - read/write
name = input("What is your name: ")

 with open("names.txt", "a") as file:
## file.write(f"{name}\n")

with open("names.txt", "r") as file:
    lines = file.readlines()

with open("names.txt", "r") as file:
    for line in lines:
        print("hello, ", line.strip())

"""

## with open("names.txt") as file:
names = []

with open("names.csv") as file:
    for line in file:
        name, house = line.rstrip().split(",")
        person = {
            "name": name,
            "house": house
        }
        names.append(person)

def get_name(person):
    return person["name"]

for person in sorted(names, key=get_name):
    print(f"{person['name']} is in {person['house']}")
        

# csv reader
"""
with open("names.csv") as file:
    reader = csv.reader(file)
    for name, home in reader:
        names.append({"name": name, "home": home})

for name in sorted(names, key=lambda x: x["name"]):
    print(f"{name['name']} is from {name['home']}")

"""
    


# =========================================
# NOTES / SUMMARY (LESSON 6: FILE I/O & CSV HANDLING)
# =========================================
#
# 1. File Modes
#    - "r" (read), "w" (write), "a" (append), "+" (read/write)
#    - Used to control how files are accessed and modified
#
# 2. File Handling with "with"
#    - Automatically opens and closes files safely
#    - Prevents memory leaks and file corruption
#
# 3. Reading Text Files
#    - read(), readlines(), and looping through file lines
#    - strip() used to clean newline characters
#
# 4. CSV File Processing (Manual)
#    - Splitting lines using .split(",")
#    - Converting raw data into structured dictionaries
#
# 5. Data Structures
#    - Storing records as a list of dictionaries
#    - Each dictionary represents one row of data
#
# 6. Sorting Data
#    - Using sorted() with a custom key function
#    - Organizing output based on specific fields (e.g., name)
#
# 7. CSV Module
#    - Using csv.reader() for cleaner and safer CSV parsing
#    - Alternative to manual string splitting
#
# 8. Lambda Functions
#    - Inline functions for quick operations (e.g., sorting keys)
#
# =========================================