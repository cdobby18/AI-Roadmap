#Unit Testing
def square(n):
    return n * n

def main():
    try:
       assert square(2) == 4
    except AssertionError:
        print("2 Squared was not 4")
    try:
        assert square(3) == 9
    except AssertionError:
        print("3 Squared was not 9")

if __name__ == "__main__":
    main()

from calculator import square

def main():
    test_square()

def test_square():
    assert square(2) == 4
    assert square(3) == 9
    
if __name__ == "__main__":
    main() 


# Unit Testing
def square(n):
    return n * n

def main():
    try:
       assert square(2) == 4
    except AssertionError:
        print("2 Squared was not 4")
    try:
        assert square(3) == 9
    except AssertionError:
        print("3 Squared was not 9")

if __name__ == "__main__":
    main()


# =========================================
# NOTES / SUMMARY (LESSON 5–6: UNIT TESTING)
# =========================================
#
# 1. Unit Testing Basics
#    - Testing individual functions (e.g., square)
#    - Verifying expected outputs using assertions
#
# 2. assert Statement
#    - Used to check if a condition is True
#    - Raises AssertionError if condition fails
#
# 3. Test Functions
#    - Creating dedicated test functions (test_square)
#    - Separating testing logic from main program
#
# 4. Modular Testing
#    - Importing functions from other files (from calculator import square)
#    - Promotes clean and reusable code structure
#
# 5. Error Handling in Tests
#    - Using try/except to catch AssertionError
#    - Printing custom error messages for failed tests
#
# 6. Entry Point Check
#    - if __name__ == "__main__":
#    - Ensures code runs only when executed directly
#
# =========================================