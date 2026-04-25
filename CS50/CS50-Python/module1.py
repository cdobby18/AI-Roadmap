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