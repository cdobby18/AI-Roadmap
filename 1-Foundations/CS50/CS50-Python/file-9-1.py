# UNPACKING
def f(*args, **kwargs):
    print("Positional: ", args)
    print("Named: ", kwargs)

f(100, 50, 25, 5)
f(galleons=100, sickles=50, knuts=25)

# MAP
def main():
    yell(["I am", "the", "Pirate King!"])

def yell(words):
    uppercased = map(str.upper, words)
    print(*uppercased)

if __name__ == "__main__":
    main() 

# LIST COMPREHENSION
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

crew = [
    pirate["name"] for pirate in pirates if pirate["crew"] == "Strawhat"
]

for crew in sorted(crew):
    print(crew)

def main():
    yell(["I am", "the", "Pirate King!"])

def yell(words):
    uppercased = [word.upper() for word in words]
    print(*uppercased)

if __name__ == "__main__":
    main()

# FILTER
# FILTER

pirates = [
    {"name": "Luffy", "crew": "Strawhat"},
    {"name": "Kaido", "crew": "Animal"},
    {"name": "Law", "crew": "Heart"},
    {"name": "Blackbeard", "crew": "Blackbeard"},
]

def is_strawhat(pirate):
    return pirate["crew"] == "Strawhat"

strawhats = filter(is_strawhat, pirates)

for pirate in strawhats:
    print(pirate["name"])

# DICTIONARY COMPREHENSION 
# DICTIONARY COMPREHENSION

pirates = [
    {"name": "Luffy", "crew": "Strawhat"},
    {"name": "Zoro", "crew": "Strawhat"},
    {"name": "Kaido", "crew": "Animal"},
]

crew_map = {
    pirate["name"]: pirate["crew"]
    for pirate in pirates
}

print(crew_map)

# GENERATORS / YIELD
def count_up(n):
    i = 1
    while i <= n:
        yield i
        i += 1

for number in count_up(5):
    print(number)

# ITERATORS
numbers = [1, 2, 3]

iterator = iter(numbers)

print(next(iterator))  # 1
print(next(iterator))  # 2
print(next(iterator))  # 3

# ENUMERATE
pirates = ["Luffy", "Zoro", "Sanji"]

for index, name in enumerate(pirates, start=1):
    print(index, name)

# =========================================
# NOTES / SUMMARY (LESSON 11: ADVANCED PYTHON TOOLS)
# =========================================
#
# 1. Unpacking (*args, **kwargs)
#    - *args collects positional arguments into a tuple
#    - **kwargs collects named arguments into a dictionary
#
#    Example:
#    def f(*args, **kwargs):
#        print(args, kwargs)
#
# 2. map()
#    - Applies a function to every item in a sequence
#    - Returns an iterator
#
#    Example:
#    map(str.upper, words)
#
# 3. List Comprehension
#    - Short, readable way to create lists
#    - Can include conditions
#
#    Example:
#    [word.upper() for word in words]
#
# 4. filter()
#    - Filters elements based on a condition
#    - Returns an iterator
#
#    Example:
#    filter(lambda p: p["crew"] == "Strawhat", pirates)
#
# 5. Dictionary Comprehension
#    - Creates dictionaries in a single line
#
#    Example:
#    {p["name"]: p["crew"] for p in pirates}
#
# 6. Generators (yield)
#    - Produces values one at a time
#    - More memory efficient than lists
#
#    Example:
#    yield i
#
# 7. Iterators
#    - Objects that can be iterated using next()
#    - Created using iter()
#
#    Example:
#    iterator = iter(list)
#    next(iterator)
#
# 8. enumerate()
#    - Adds index to iterable items
#    - Useful for loops needing position + value
#
#    Example:
#    for i, value in enumerate(list)
#
# =========================================