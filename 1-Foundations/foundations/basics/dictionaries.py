person = {"name": "Carl", "age": 25, "city": "Bongabon"}

# Access value
print(person["name"])

# Update value
person["age"] = 26

# Add new key
person["country"] = "Philippines"

# Remove key
del person["city"]

print(person)