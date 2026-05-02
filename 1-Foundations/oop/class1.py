class Employee:
    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = f"{first.lower()}.{last.lower()}@gmail.com"

    def fullname(self):
        return f"{self.first} {self.last}"
    
    def apply_raise(self, percent):
        self.pay = int(self.pay * (1 + percent))


emp_1 = Employee('Luffy', 'Dragon', 300000)
emp_2 = Employee('Roronoa', 'Zoro', 100000)

print(emp_1.first)
print(emp_1.email)
print(emp_2.pay)

print(emp_1.fullname())
print(emp_2.fullname())

emp_2.apply_raise(0.10)
print(emp_2.pay)


# =========================================
# 📘 CLASSES AND INSTANCES — COMMENT NOTES
# =========================================

# 🧠 CLASS
# A class is a blueprint/template for creating objects.

# 👤 INSTANCE
# An instance is an actual object created from a class.

# ⚙️ __init__ (CONSTRUCTOR)
# Automatically runs when creating an object.
# Used to initialize attributes.

# 🧾 ATTRIBUTES
# Variables inside a class (data of the object).
# Example: first, last, pay, email

# 🧩 METHODS
# Functions inside a class (behavior of the object).
# Example: fullname(), apply_raise()

# 🔑 self
# Refers to the current instance of the class.
#
# =========================================

