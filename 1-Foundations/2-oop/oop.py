from abc import ABC, abstractmethod


# --------------------------------
# ABSTRACTION
# --------------------------------
# Abstract class (cannot be instantiated directly)
class Person(ABC):

    def __init__(self, name, age):
        self.name = name
        self._age = age   # Encapsulation (protected attribute)

    @abstractmethod
    def role(self):
        pass


# --------------------------------
# INHERITANCE
# --------------------------------
class Student(Person):

    def __init__(self, name, age, scores):
        # super() calls the parent constructor
        super().__init__(name, age)
        self.scores = scores

    # POLYMORPHISM
    def role(self):
        return "Student"

    def compute_average(self):
        total = sum(self.scores.values())
        avg = total / len(self.scores)
        return avg

    def display_info(self):
        avg = self.compute_average()
        print(f"{self.name} | Role: {self.role()} | Average: {avg:.2f}")


class Teacher(Person):

    def __init__(self, name, age, subject):
        super().__init__(name, age)
        self.subject = subject

    # POLYMORPHISM
    def role(self):
        return "Teacher"

    def display_info(self):
        print(f"{self.name} | Role: {self.role()} | Subject: {self.subject}")


# --------------------------------
# ENCAPSULATION
# --------------------------------
class BankAccount:

    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance  # private attribute

    def deposit(self, amount):
        self.__balance += amount

    def withdraw(self, amount):
        if amount <= self.__balance:
            self.__balance -= amount
        else:
            print("Insufficient balance")

    def get_balance(self):
        return self.__balance


# --------------------------------
# MAIN PROGRAM
# --------------------------------

scores = {
    "Math": 90,
    "Science": 85,
    "English": 88
}

student1 = Student("Carl", 23, scores)
teacher1 = Teacher("Dr. Smith", 40, "Mathematics")

student1.display_info()
teacher1.display_info()

account = BankAccount("Carl", 1000)

account.deposit(500)
account.withdraw(200)

print("Remaining Balance:", account.get_balance())