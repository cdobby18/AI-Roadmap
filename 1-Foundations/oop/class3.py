# classMethods - staticMethods
import datetime

class Employee:

    numOfEmps = 0
    raise_amount = 1.04

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = f"{first.lower()}.{last.lower()}@gmail.com"

        Employee.numOfEmps += 1

    # Instance Method
    def fullname(self):
        return f"{self.first} {self.last}"

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)

    # Class Method
    @classmethod
    def set_raise_amount(cls, amount):
        cls.raise_amount = amount

    # Alternative Constructor (Class Method)
    @classmethod
    def from_string(cls, emp_str):
        first, last, pay = emp_str.split("-")
        return cls(first, last, int(pay))

    # Static Method
    @staticmethod
    def is_workday(day):
        return day.weekday() < 5

# Create employees
emp_1 = Employee('Luffy', 'Dragon', 300000)
emp_2 = Employee('Zoro', 'Roronoa', 100000)

# Instance method
print(emp_1.fullname())

# Apply raise
Employee.set_raise_amount(1.10)
emp_1.apply_raise()
print(emp_1.pay)

# Alternative constructor
emp_str = "Sanji-Vinsmoke-200000"
emp_3 = Employee.from_string(emp_str)
print(emp_3.email)

# Static method (with date shown)
my_date = datetime.date(2026, 5, 2)

print(f"Date: {my_date}")
print(f"Is workday? {Employee.is_workday(my_date)}")

# Optional: readable message
if Employee.is_workday(my_date):
    print(f"{my_date} is a workday")
else:
    print(f"{my_date} is NOT a workday")