numbers = [10, 20, 30, 40]
names = ["Alice", "Bob", "Carl"]

# Access elements
print(numbers[0])  # 10
print(names[-1])   # Carl (negative indexing)

# Modify elements
numbers[1] = 25

# Add elements
numbers.append(50)        # Add to end
numbers.insert(2, 27)     # Insert at index 2

# Remove elements
numbers.remove(30)        # Remove by value
last_item = numbers.pop() # Remove last element

print(numbers, last_item)