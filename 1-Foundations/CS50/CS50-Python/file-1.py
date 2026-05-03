# user input
name = input("What's your name: ")
name = name.strip()
name = name.title()
name = name.capitalize()

print(f"Name: {name}")

x = int(input("Enter x: "))
y = int(input("Enter y: "))

z = x + y
print(f"Result: {z}")

# function
def main():
    a = int(input("What is X: "))
    if is_even(a):
        print("Even") 
    else:
        print("Odd")

def is_even(n):
    return n % 2 == 0

main()

# conditionals
score = int(input("Enter score:"))

if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
else:
    print("Grade: D")    

# =========================================
# NOTES / SUMMARY (FILE 1: INTRODUCTION)
# =========================================
#
# 1. User Input & Strings
#    - Using input() to collect data from users
#    - Cleaning and formatting strings using strip(), title(), capitalize()
#
# 2. Data Types & Type Casting
#    - Converting input values into integers using int()
#
# 3. Basic Operations
#    - Performing arithmetic operations (addition)
#
# 4. Functions
#    - Creating reusable functions (main, is_even)
#    - Using return values for logic
#
# 5. Conditionals
#    - Using if-elif-else for decision making
#    - Applying logical comparisons (grading system, even/odd check)
#
# =========================================