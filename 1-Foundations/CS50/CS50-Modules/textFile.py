# Write
with open("example.txt", "w") as f:
    f.write("Hello Python\nSecond line")

# Read
with open("example.txt", "r") as f:
    print(f.read())