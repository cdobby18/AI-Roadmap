#FILE I/O
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
    


