import argparse

# SET
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

crews = set()

for pirate in pirates:
    crews.add(pirate["crew"])


for crew in sorted(crews):
    print(crew)

# GLOBAL
class Account:
    def __init__(self):
        self._balance = 0

    @property
    def balance(self):
        return self._balance 
    
    def deposit(self, n):
        self._balance += n

    def withdraw(self, n):
        self._balance -= n

def main():
    account = Account()
    print("Balance: ", account.balance) 
    account.deposit(100)
    account.withdraw(50)
    print("Balance: ", account.balance)

if __name__ == "__main__":
    main()

# Constants
class Luffy:

    GUM = 3

    def gum(self):
        for _ in range(Luffy.GUM):
            print("Gum Gum No!")

luffy = Luffy()
luffy.gum()

# Doctsring
class Account:
    """
    Represents a simple bank account.
    """

    def __init__(self) -> None:
        """
        Initialize account with zero balance.
        """
        self._balance: int = 0

    @property
    def balance(self) -> int:
        """
        Return current balance.
        """
        return self._balance

    def deposit(self, n: int) -> None:
        """
        Deposit amount n into account.
        """
        self._balance += n

    def withdraw(self, n: int) -> None:
        """
        Withdraw amount n from account.
        """
        self._balance -= n

# ARGPARSE

def main() -> None:
    parser = argparse.ArgumentParser(description="Simple Bank Account")

    parser.add_argument("--deposit", type=int, default=0, help="Amount to deposit")
    parser.add_argument("--withdraw", type=int, default=0, help="Amount to withdraw")

    args = parser.parse_args()

    account = Account()

    account.deposit(args.deposit)
    account.withdraw(args.withdraw)

    print("Balance:", account.balance)

# =========================================
# NOTES / SUMMARY (LESSON 10: SETS, OOP, TYPE HINTS, DOCSTRINGS, ARGPARSE)
# =========================================
#
# 1. Sets
#    - A set is a collection of unique values (no duplicates)
#    - Useful for removing duplicate data (e.g., pirate crews)
#    - Unordered, but can be sorted using sorted()
#
#    Example:
#    crews = set()
#    crews.add("Strawhat")
#
# 2. Looping & Data Extraction
#    - Iterating through a list of dictionaries to extract values
#    - Used to collect specific fields (e.g., crew names)
#
#    Example:
#    for pirate in pirates:
#        crews.add(pirate["crew"])
#
# 3. Object-Oriented Programming (OOP)
#    - Uses classes and objects to structure programs
#    - Promotes reusable and organized code
#
# 4. Classes & Constructors
#    - A class is a blueprint (e.g., Account)
#    - __init__ initializes object attributes
#
#    Example:
#    class Account:
#        def __init__(self):
#            self._balance = 0
#
# 5. Encapsulation
#    - Uses "_" to indicate protected variables (e.g., _balance)
#    - Prevents direct modification from outside the class
#
# 6. Properties (@property)
#    - Allows controlled access to attributes
#    - Acts like a variable but runs a method
#
#    Example:
#    @property
#    def balance(self):
#        return self._balance
#
# 7. Methods
#    - deposit(): adds money
#    - withdraw(): subtracts money
#
#    Example:
#    account.deposit(100)
#
# 8. Constants
#    - Values that should not change
#    - Written in ALL CAPS by convention
#
#    Example:
#    GUM = 3
#
# 9. Type Hints
#    - Specifies expected data types
#    - Helps tools like mypy detect errors
#    - Improves readability and debugging
#
#    Example:
#    def deposit(self, n: int) -> None:
#
# 10. Docstrings
#     - Used to document classes and functions
#     - Explains purpose and behavior of code
#     - Accessible via help()
#
#     Example:
#     """Deposit amount n into account."""
#
# 11. Argparse (Command-Line Arguments)
#     - Allows user input from the terminal
#     - Makes programs flexible and interactive
#
#     Example:
#     python app.py --deposit 100 --withdraw 50
#
#     Key Parts:
#     - ArgumentParser(): creates parser
#     - add_argument(): defines inputs
#     - parse_args(): reads user input
#
# 12. Main Function Pattern
#     - Uses if __name__ == "__main__"
#     - Ensures main() runs only when file is executed directly
#
# =========================================