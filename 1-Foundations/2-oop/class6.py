# Property Decorators - Getters, Setters, and Deleters

# =========================
# Pirate Class
# =========================
class Pirate:

    def __init__(self, first, last):
        self.first = first
        self.last = last

    # Getter
    @property
    def fullname(self):
        return f"{self.first} {self.last}"

    @property
    def bounty_poster(self):
        return f"{self.first.lower()}.{self.last.lower()}@pirate.com"

    # Setter
    @fullname.setter
    def fullname(self, name):
        first, last = name.split(" ")
        self.first = first
        self.last = last

    # Deleter
    @fullname.deleter
    def fullname(self):
        print("Identity removed! ☠️")
        self.first = None
        self.last = None


# =========================
# Testing
# =========================

# Create pirate
pirate_1 = Pirate("Luffy", "Monkey")

# Getter
print(pirate_1.fullname)
print(pirate_1.bounty_poster)

print()

# Setter (updates first & last automatically)
pirate_1.fullname = "Zoro Roronoa"
print(pirate_1.fullname)
print(pirate_1.bounty_poster)

print()

# Deleter
del pirate_1.fullname
print(pirate_1.first)
print(pirate_1.last)