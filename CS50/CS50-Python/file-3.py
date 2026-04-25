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
    print("❌ That file does not exist.")
except PermissionError:
    print("❌ You don't have permission to read this file.")