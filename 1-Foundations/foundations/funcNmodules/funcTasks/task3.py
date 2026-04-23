# Task 11: Save 10 Random Numbers to a File and Sum Them

import random

# Generate 10 random numbers
numbers = [random.randint(1, 100) for _ in range(10)]

# Save numbers to a file
with open("numbers.txt", "w") as f:
    for num in numbers:
        f.write(f"{num}\n")

# Read numbers from file and sum them
with open("numbers.txt", "r") as f:
    read_numbers = [int(line.strip()) for line in f]

total = sum(read_numbers)
print("Numbers:", read_numbers)
print("Total:", total)