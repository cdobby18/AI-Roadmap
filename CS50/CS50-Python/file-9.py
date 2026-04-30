# SET
pirates = [
    {"name": "Luffy", "crew": "Strawhat"},
    {"name": "Kaido", "crew": "Animal"},
    {"name": "Law", "crew": "Heart"},
    {"name": "Blackbeard", "crew": "Blackbeard"},
    {"name": "Garp", "crew": "Marine"},
    {"name": "Linlin", "crew": "Big Mom"},
    {"name": "Shanks", "crew": "Red Haired"},
    {"name": "Whitebeard", "crew": "Whitebeard"},
    {"name": "Roger", "crew": "Roger"},
    {"name": "Rocks", "crew": "Xebec"}
]

crews = set()

for pirate in pirates:
    crews.add(pirate["crew"])


for crew in sorted(crews):
    print(crew)

# GLOBAL
berry = 0

def main():
    print("Berry: ", berry)
    deposit(100)
    withdraw(50)
    print("Berry: ", berry)

def deposit(n):
    global berry
    berry += n

def withdraw(n):
    global berry
    berry -= n

if __name__ == "__main__":
    main()