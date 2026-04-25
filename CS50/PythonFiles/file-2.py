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
    print(pirate["name"], pirate["crew"], sep=", ")