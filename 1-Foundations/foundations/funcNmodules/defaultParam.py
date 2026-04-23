# Function to greet a user
def greet(name="Guest"):
    return f"Hello, {name}!"

# Function to calculate total, count, and average of a list
def stats(nums):
    total = sum(nums)
    count = len(nums)
    avg = total / count
    return total, count, avg

# Main program
if __name__ == "__main__":
    # Greet the user
    user_name = input("Enter your name: ")
    print(greet(user_name))

    # Get numbers from the user
    numbers_input = input("Enter numbers separated by spaces: ")
    numbers = [float(x) for x in numbers_input.split()]

    # Calculate stats
    total, count, avg = stats(numbers)

    # Display results
    print(f"Numbers entered: {numbers}")
    print(f"Total: {total}")
    print(f"Count: {count}")
    print(f"Average: {avg}")