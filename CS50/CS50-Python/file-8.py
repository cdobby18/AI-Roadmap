# Classes
class Pirate:
    def __init__(self, first, middle, last, crew):

        if not first or not last:
            raise ValueError("Missing Name")

        crew = crew.strip().title()

        if crew not in ["Strawhat", "Heart", "Animals", "Big Mom"]:
            raise ValueError("Invalid Crew")

        self._first = first.strip().title()
        self._middle = middle.strip().title()
        self._last = last.strip().title()
        self._crew = crew

    def full_name(self):
        if self._middle:
            return f"{self._first} {self._middle} {self._last}"
        return f"{self._first} {self._last}"

    def __str__(self):
        return f"{self.full_name()} from {self._crew}"

    # Properties

    @property
    def first(self):
        return self._first

    @first.setter
    def first(self, value):
        self._first = value.strip().title()

    @property
    def middle(self):
        return self._middle

    @middle.setter
    def middle(self, value):
        self._middle = value.strip().title()

    @property
    def last(self):
        return self._last

    @last.setter
    def last(self, value):
        self._last = value.strip().title()

    @property
    def crew(self):
        return self._crew

    @crew.setter
    def crew(self, value):
        value = value.strip().title()

        if value not in ["Strawhat", "Heart", "Animals", "Big Mom"]:
            raise ValueError("Invalid Crew")

        self._crew = value

def main():
    pirate = get_student()
    print(pirate)

def get_student():
    first = input("First Name: ")
    middle = input("Middle Name (optional): ")
    last = input("Last Name: ")

    while True:
        crew = input("Crew: ").strip().title()
        if crew in ["Strawhat", "Heart", "Animals", "Big Mom"]:
            break
        print("Invalid crew. Try again.")

    return Pirate(first, middle, last, crew)

if __name__ == "__main__":
    main()


# =========================================
# NOTES / SUMMARY (LESSON 8: CLASSES & OBJECT-ORIENTED PROGRAMMING)
# =========================================
#
# 1. Classes (Blueprints for Objects)
#    - A class defines a custom data type (e.g., Pirate)
#    - Objects are instances of a class
#
# 2. Constructor (__init__)
#    - Runs automatically when an object is created
#    - Used to initialize attributes (first, middle, last, crew)
#
# 3. Data Validation
#    - Ensures required fields exist (first, last)
#    - Restricts allowed values (crew must be valid)
#    - Uses ValueError to handle invalid input
#
# 4. Encapsulation
#    - Attributes use "_" prefix (e.g., _first)
#    - Protects internal data from direct modification
#
# 5. Methods
#    - full_name(): returns formatted name
#    - __str__(): defines how object is printed
#
# 6. Properties (Getters & Setters)
#    - @property allows controlled access to attributes
#    - @setter allows validation before updating values
#    - Keeps data safe and consistent
#
# 7. Input Handling
#    - Uses loops to ensure valid user input (crew selection)
#    - Keeps program from crashing due to bad input
#
# 8. Object Creation Flow
#    - User inputs data → validation → Pirate object created → printed
#
# Overall:
# This lesson introduces Object-Oriented Programming (OOP),
# focusing on creating structured, reusable, and safe data models
# using classes, methods, and encapsulation.
# =========================================