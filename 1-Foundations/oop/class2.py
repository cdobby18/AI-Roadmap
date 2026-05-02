# Class Variables
class Employee:

    numOfEmps = 0
    raise_amount = 1.04

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = f"{first.lower()}.{last.lower()}@gmail.com"

        Employee.numOfEmps += 1

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
#  LESSON 2: CLASS VARIABLES — NOTES
# =========================================

# Instance Variables:
# - Unique to each object
# - Defined using self (inside __init__)
# Example: first, last, pay, email

# Class Variables:
# - Shared across all objects
# - Defined at the class level
# Example: numOfEmps, raise_amount

# =========================================
#  ACCESSING CLASS VARIABLES
# =========================================

# Access via class (recommended)
# Employee.numOfEmps

# Access via instance (works, but not best practice)
# emp_1.numOfEmps

# =========================================
#  MODIFYING CLASS VARIABLES
# =========================================
#
# Modify using class:
# Employee.raise_amount = 1.05
#
# =========================================