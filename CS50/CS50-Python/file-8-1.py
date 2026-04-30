import random

class DevilFruit:
    def __init__(self, name, type_, power):                              
        self.name = name.title()
        self.type = type_.title()
        self._power = power   # encapsulated (protected style)

    # =========================
    # PROPERTY (Encapsulation)
    # =========================
    @property
    def power(self):
        return self._power

    @power.setter
    def power(self, value):
        if value < 0:
            raise ValueError("Power cannot be negative")
        self._power = value

    # =========================
    # INSTANCE METHOD
    # =========================
    def describe(self):
        return f"{self.name} ({self.type}) - Power: {self.power}"

    def is_stronger_than(self, other):
        return self.power > other.power

    def fuse_with(self, other):
        return DevilFruit(
            f"{self.name}-{other.name}",
            "Hybrid",
            self.power + other.power
        )

    # =========================
    # OPERATOR OVERLOADING
    # =========================
    def __add__(self, other):
        return self.fuse_with(other)

    def __eq__(self, other):
        return self.power == other.power

    def __str__(self):
        return self.describe()

    # =========================
    # CLASS METHOD
    # =========================
    @classmethod
    def random_fruit(cls, name):
        types = ["Paramecia", "Zoan", "Logia"]
        return cls(
            name,
            random.choice(types),
            random.randint(10, 100)
        )

# =========================
# INHERITANCE
# =========================
class SpecialFruit(DevilFruit):
    def __init__(self, name, type_, power, ability):
        super().__init__(name, type_, power)
        self.ability = ability

    # METHOD OVERRIDING
    def describe(self):
        return f"{super().describe()} | Ability: {self.ability}"


# =========================
# STATIC METHOD
# =========================
class FruitUtils:
    @staticmethod
    def is_legendary(power):
        return power > 90

# Random fruits (class method)
fruit1 = DevilFruit.random_fruit("Gum Gum")
fruit2 = DevilFruit.random_fruit("Flame Flame")

print("Fruit 1:", fruit1)
print("Fruit 2:", fruit2)

# Comparison (custom method)
print("\nStronger?", fruit1.is_stronger_than(fruit2))

# Operator overloading (+)
fusion = fruit1 + fruit2
print("\nFusion:", fusion)

# Equality operator
print("\nSame power?", fruit1 == fruit2)

# Encapsulation (property setter/getter)
fruit1.power += 5
print("\nUpgraded Fruit 1:", fruit1.power)

# Inheritance + overriding
special = SpecialFruit("Dark Dark", "Logia", 95, "Gravity Control")
print("\nSpecial:", special)

# Static method
print("\nIs Legendary?", FruitUtils.is_legendary(special.power))

# =========================================
# NOTES / SUMMARY (LESSON 9: ADVANCED OOP)
# =========================================
#
# 1. Encapsulation (Private-like Attributes)
#    - Uses _power to protect data
#    - Controlled access via @property and @setter
#    - Prevents invalid values (e.g., negative power)
#
# 2. Instance Methods
#    - Functions that operate on object data
#    - Example: describe(), is_stronger_than(), fuse_with()
#
# 3. Operator Overloading
#    - Custom behavior for operators like + and ==
#    - __add__ → combines two objects
#    - __eq__ → compares object values
#    - __str__ → controls print output
#
# 4. Class Methods
#    - @classmethod creates alternative constructors
#    - Example: random_fruit() generates random DevilFruit
#
# 5. Inheritance
#    - SpecialFruit inherits from DevilFruit
#    - Reuses and extends parent class functionality
#
# 6. Method Overriding
#    - Child class modifies parent method (describe)
#    - Uses super() to reuse parent logic
#
# 7. Static Methods
#    - Utility functions not tied to instance data
#    - Example: is_legendary(power)
#
# 8. Object Interactions
#    - Comparing, combining, and modifying objects
#    - Demonstrates real-world modeling using OOP
#
# Overall:
# This lesson shows advanced Object-Oriented Programming concepts
# including inheritance, polymorphism, encapsulation, and operator overloading,
# enabling more powerful and flexible program design.
# =========================================