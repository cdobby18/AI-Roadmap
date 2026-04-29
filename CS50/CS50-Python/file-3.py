# Exceptions

def main():
    x = get_int()
    print(f"The value of x is: {x}")

def get_int(prompt):
    while True: 
        try:
            return int(input(prompt))
        except ValueError: #Value Error
            print("x is not an integer")
            # pass (another error handling keyword)

main()

# Multiple exceptions
try:
    a = int(input("Enter numerator: "))
    b = int(input("Enter denominator: "))
    result = a / b
    print("Result:", result)

except ValueError:
    print("Please enter valid integers only.")

except ZeroDivisionError:
    print("Cannot divide by zero.")

# Finally
try:
    file = open("data.txt", "r")
    content = file.read()

except FileNotFoundError:
    print("File not found.")

finally:
    print("This always runs (cleanup step).")

# File Handling
filename = input("Enter filename: ")

try:
    with open(filename, "r") as file:
        print(file.read())

except FileNotFoundError:
    print("That file does not exist.")
except PermissionError:
    print("You don't have permission to read this file.")


# =========================================
# NOTES / SUMMARY (LESSON 3: EXCEPTIONS & FILE HANDLING)
# =========================================
#
# 1. Exceptions (try-except)
#    - Used to prevent program crashes from runtime errors
#    - try block contains risky code
#    - except handles specific errors (e.g., ValueError)
#
# 2. Input Validation with Exceptions
#    - Repeatedly ask for input until valid (loop + try/except)
#    - Ensures program stability and user-friendly behavior
#
# 3. Multiple Exceptions
#    - Handling different error types separately
#    - Example: ValueError (invalid input), ZeroDivisionError (division by zero)
#
# 4. finally Block
#    - Code that always executes, regardless of errors
#    - Commonly used for cleanup operations
#
# 5. File Handling
#    - Reading files using open() and with statement
#    - "with" ensures automatic file closing (best practice)
#
# 6. File-related Exceptions
#    - FileNotFoundError → file does not exist
#    - PermissionError → no access rights
#
# =========================================