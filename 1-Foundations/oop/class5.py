# Class Special Methods

# =========================
# 🍈 Devil Fruit Class
# =========================
class DevilFruit:

    def __init__(self, name, user, power_level, abilities):
        self.name = name
        self.user = user
        self.power_level = power_level
        self.abilities = abilities  # list of abilities

    # Readable (for users)
    def __str__(self):
        return f"{self.name} eaten by {self.user} | Power: {self.power_level}"

    # Developer view (debugging)
    def __repr__(self):
        return f"DevilFruit('{self.name}', '{self.user}', {self.power_level}, {self.abilities})"

    # Combine two fruits (add power levels)
    def __add__(self, other):
        return self.power_level + other.power_level

    # Length of abilities
    def __len__(self):
        return len(self.abilities)

    # Compare equality (same power level)
    def __eq__(self, other):
        return self.power_level == other.power_level

    # Less than (for sorting)
    def __lt__(self, other):
        return self.power_level < other.power_level

# Objects
gomu = DevilFruit(
    "Gomu Gomu no Mi",
    "Luffy",
    95,
    ["Stretch", "Gear 2", "Gear 5"]
)

mera = DevilFruit(
    "Mera Mera no Mi",
    "Ace",
    90,
    ["Fire Fist", "Flame Control"]
)

yami = DevilFruit(
    "Yami Yami no Mi",
    "Blackbeard",
    98,
    ["Darkness", "Gravity Pull"]
)

# =========================
# Outputs
# =========================

# __str__
print(gomu)

# __repr__
print(repr(gomu))

print()

# __add__
print("Combined Power:", gomu + mera)

# __len__
print("Abilities of Gomu:", len(gomu))

print()

# __eq__
print("Gomu == Mera:", gomu == mera)

# __lt__
print("Gomu < Yami:", gomu < yami)

print()

# Sorting using __lt__
fruits = [gomu, mera, yami]
fruits.sort()

print("Sorted by Power Level:")
for fruit in fruits:
    print(fruit)