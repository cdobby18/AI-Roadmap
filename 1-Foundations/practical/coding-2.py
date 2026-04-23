print("====================================")
# PALINDROME CHECKER

def is_palindrome(word):
    left = 0
    right = len(word) - 1

    while left < right:
        if word[left] != word[right]:
            return False
        left += 1
        right -= 1
        
    return True
print(is_palindrome("racecar"))  
print(is_palindrome("level"))    
print(is_palindrome("python"))

print("====================================")
# WORD LENGTH ANALYZER

sentence = "artificial intelligence will change the world"

words = sentence.split()

for word in words:
    print(word, "->", len(word))

print("====================================")
# REVERSE LIST

data = [1,2,3,4]
reversed_data = data[::-1]

print(reversed_data)


print("====================================")
# EVEN NUMBERS

numbers = [1,2,3,4,5,6,7,8,9,10]

even_numbers = [val for val in numbers if val % 2 == 0]

odd_numbers = []

for val in numbers:
    if val % 2 != 0:
        odd_numbers.append(val)

print("Even Numbers:", even_numbers)
print("Odd Numbers:", odd_numbers)


print("====================================")
# DUPLICATE NUMBERS

original_list = [1,2,2,3,4,3,5]

unique_list = []

for item in original_list:
    if item not in unique_list:
        unique_list.append(item)

print("List with duplicates removed:", unique_list)


print("====================================")
# RECOMMENDATION FILTER (FINAL PROJECT)

products = ["laptop", "phone", "tablet", "phone", "laptop"]

count_products = {}

for product in products:
    if product in count_products:
        count_products[product] += 1
    else:
        count_products[product] = 1

print("Product frequency:")

for product, count in count_products.items():
    print(f"{product}: {count}")


unique_products = []

for item in products:
    if item not in unique_products:
        unique_products.append(item)

print("Products with duplicates removed:", unique_products)
print("Product count:", len(unique_products))

print("====================================")
# OOP

class Student():
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade

    def introduce(self):
        print(f"Hello, my name is {self.name}. I am {self.age} years old and my grades are {self.grade}.")

    def calculate_average(self):
        total = sum(self.grade.values())
        avg = total / len(self.grade)
        return avg
    
    def display_info(self):
        avg = self.calculate_average()
        print(f"Average: {avg:.2f}")
    
grade = {
    "Math": 90,
    "Science": 85,
    "English": 88,
    "Physical Education": 88,
    "Arts": 88,
}

grade2 = {
    "Math": 92,
    "Science": 82,
    "English": 84,
    "Physical Education": 86,
    "Arts": 88,
}

grade3 = {
    "Math": 91,
    "Science": 87,
    "English": 88,
    "Physical Education": 89,
    "Arts": 94,
}

s1 = Student("Carl", 22, grade)
s2 = Student("Joshua", 23, grade2)
s3 = Student("CJ", 22, grade3)

s1.display_info()
s2.display_info()
s3.display_info()

print("====================================")
# DSA TOPICS

data = [4,8,15,16,23,42]

print(sum(data))
print(max(data))
print(min(data))

# REVERSE A LIST
numbers = [1,2,3,4,5]
reversed_list = []

for i in range(len(numbers)-1, -1, -1):
    reversed_list.append(numbers[i])

print(reversed_list)

# PAIR TWO SUMS COMBINATIONS
numbs = [5,4,3,2,1]
target = 5
pairs = []

seen = set()

for num in numbs:
    complement = target - num
    if complement in seen:
        pairs.append((complement, num))
    seen.add(num)

print(pairs)

print("====================================")
# REMOVE DUPLICATES

datas = [1,2,2,3,4,4,5]
unique_data = []

for item in datas:
    if item not in unique_data:
        unique_data.append(item)

print(unique_data)

print("====================================")
# FREQUENCY COUNTER + TWO SUM

numData = [1,2,2,3,3,3,4]
frequency = {}
target = 6
paired = []

seen = set()

# Frequency Counter
for num in numData:
    if num in frequency:
        frequency[num] += 1
    else:
        frequency[num] = 1

# Find pairs that sum to target
for num in numData:
    needed = target - num

    if needed in seen:
        paired.append((needed, num))

    seen.add(num)

print(f"Frequency Counter: {frequency}")
print(f"Pairs that sum to {target}: {paired}")

print("====================================")
# FIRST NON-REPEATING ELEMENT

nums = [4, 5, 1, 2, 0, 4]

# num count
frequency = {}
for num in nums:
    if num in frequency:
        frequency[num] += 1
    else:
        frequency[num] = 1

# non repeat
first_unique = None
for num in nums:
    if frequency[num] == 1:
        first_unique = num
        break

print(f"First Non-Repeating Element: {first_unique}")
