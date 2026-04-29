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