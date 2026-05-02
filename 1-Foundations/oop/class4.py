# Inheritance = subclasses

# =========================
# Base Class
# =========================
class Character:

    def __init__(self, name, bounty):
        self.name = name
        self.bounty = bounty

    def show_info(self):
        return f"Name: {self.name} | Bounty: {self.bounty} berries"

    def increase_bounty(self, amount):
        self.bounty += amount

# =========================
# Subclass: Pirate
# =========================
class Pirate(Character):

    def __init__(self, name, bounty, crew, role):
        super().__init__(name, bounty)
        self.crew = crew
        self.role = role

    # Method override
    def show_info(self):
        return f"{self.name} ({self.role}) of {self.crew} Pirates | Bounty: {self.bounty}"

    def attack(self):
        print(f"{self.name} attacks with pirate skills! ⚔️")

# =========================
# Subclass: Marine
# =========================
class Marine(Character):

    def __init__(self, name, bounty, rank):
        super().__init__(name, bounty)
        self.rank = rank

    def show_info(self):
        return f"{self.name} [{self.rank}] | Target Bounty: {self.bounty}"

    def capture(self):
        print(f"{self.name} is capturing pirates! 🚔")

# =========================
# Subclass: Revolutionary
# =========================
class Revolutionary(Character):

    def __init__(self, name, bounty, army):
        super().__init__(name, bounty)
        self.army = army

    def show_info(self):
        return f"{self.name} from {self.army} Army | Bounty: {self.bounty}"

    def revolt(self):
        print(f"{self.name} leads a revolution! 🔥")

# Objects
luffy = Pirate("Luffy", 3000000000, "Strawhat", "Captain")
garp = Marine("Garp", 0, "Vice Admiral")
dragon = Revolutionary("Dragon", 5000000000, "Revolutionary")

# Show info
print(luffy.show_info())
print(garp.show_info())
print(dragon.show_info())

# Actions
luffy.attack()
garp.capture()
dragon.revolt()

# Increase bounty
luffy.increase_bounty(500000000)
print(f"Updated Bounty of {luffy.name}: {luffy.bounty}")


