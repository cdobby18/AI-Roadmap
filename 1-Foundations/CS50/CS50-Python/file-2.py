# while loop
i = 0

while i <=3:
    print("meow")
    i += 1

# for loop

for i in[0,1,2]:
    print("arf")

while True:
    n = int(input("What's N: "))
    if n > 0:
        break

for _ in range(n):
    print("hi")

def main():
    number = get_number()
    hello(number)

def get_number():
    while True:
        a = int(input("What's A? "))
        if a > 0:
            break
        return a
    
def hello(a):
    for _ in range (a):
        print("Hello!")

# List Iteration
students = ["Luffy", "Zoro", "Sanji"]

for student in students:
    print(student)

chars = ["Nami", "Robin", "Chopper"]

for i in range(len(chars)):
    print(chars[i])

pirates = [
    {"name": "Luffy", "crew": "Strawhat"},
    {"name": "Zoro", "crew": "Strawhat"},
    {"name": "Sanji", "crew": "Strawhat"},
    {"name": "Jinbei", "crew": "Strawhat"},
]

for pirate in pirates:
    print(pirate["name"], pirate["crew"])


# =========================================
# NOTES / SUMMARY (LESSON 2: LOOPS & ITERATION)
# =========================================
#
# 1. While Loops
#    - Used when the number of iterations is unknown
#    - Controlled using conditions (e.g., i <= 3)
#    - Infinite loops (while True) with break for control
#
# 2. For Loops
#    - Used for iterating over sequences (lists, ranges)
#    - range() is commonly used for repeated execution
#    - "_" is used as a throwaway variable when index is not needed
#
# 3. Input Validation
#    - Ensuring user inputs meet conditions (e.g., positive numbers)
#    - Loop continues until valid input is given
#
# 4. Functions with Loops
#    - Separating logic into reusable functions (main, get_number, hello)
#    - Combining loops with functions for structured programs
#
# 5. Lists & Iteration
#    - Iterating directly over list elements
#    - Using index-based iteration with range(len())
#
# 6. Dictionaries in Lists
#    - Storing structured data (list of dictionaries)
#    - Accessing values using keys (e.g., pirate["name"])
#
# =========================================