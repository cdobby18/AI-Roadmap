# Task 10: Calculator Program with Functions in a Module
import calculator  # Import the module we created

a = float(input("Enter first number: "))
b = float(input("Enter second number: "))

print("Add:", calculator.add(a, b))
print("Subtract:", calculator.subtract(a, b))
print("Multiply:", calculator.multiply(a, b))
print("Divide:", calculator.divide(a, b))