""" 
Task 1. Profile Generator CLI: DONE

    - create a program that asks user input (name, age, goal) and prints a formatted AI Engineer Profile

    Output:
        - Enter name: John
          Enter age: 21
          Enter goal: AI Engineer

          --- PROFILE ---
          Name: John
          Age: 21
          Goal: AI Engineer
          Status: Learning Python

Task 2. Calculator CLI System: Done
    
    - build cli calculator system that performs +,-,*,/ using functions

    Output:
        Enter first number: 10
        Enter operator: -
        Enter second number: 5

        Result: 5

Task 3. Grade Classification System:

    - input score (0 - 100), return letter grade.

    Output:
        Score: 87
        Grade: B

Task 4. Even Number Filter System

    - print 0 to 100 but only even numbers excluding multiples of 3

    Output:
        2 4 8 10 14 16

"""

# Task 1
name = input("Enter name: ")
age = input("Enter age: ")
goal = input("Enter goal: ")

print("==== PROFILE =====")
print(f"Name: {name}")
print(f"Age: {age}")
print(f"Goal: {goal}")
print("Status: Learning Python")

# Task 2
first = int(input("Enter first number: "))
operator = input("Enter operator: ")
second = int(input("Enter second number: "))

if operator == "+":
    result = first + second
    print(result)
elif operator == "-":
    result = first - second
    print(result)
elif operator == "*":
    result = first * second
    print(result)
elif operator == "/":
    result = first / second
    print(result)
else:
    print("Invalid Operator")

# Task 3
grade = int(input("Enter Grade: "))

if grade >= 81 and grade <= 100:
    print("Grade: A")

elif grade >= 61 and grade <= 80:
    print("Grade: B")

elif grade >= 41 and grade <= 60:
    print("Grade: C")

elif grade >= 21 and grade <= 40:
    print("Grade: D")

elif grade >= 1 and grade <= 20:
    print("Grade: F")

# Task 4
for i in range (1, 101):
    if i % 2 == 0  and i % 3 != 0:
        print(i)