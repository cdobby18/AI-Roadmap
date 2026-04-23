
# Task 9: Function to calculate factorial.
def factorial(n):
    result = 1
    
    for i in range(1, n + 1):
        result = result * i
    
    return result


# Test the function
num = 5
print("Factorial of", num, "is", factorial(num))