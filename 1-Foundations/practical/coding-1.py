print ("====================================")
# STARS

rows = 5 
for i in range(1, rows + 1):
    print("*" * i, end="\n")

print ("====================================")
# SUM OF 1 TO 100

total = 0

for number in range(1,101):
    total += number

print("Total Sum: ", total)

print ("====================================")
# LARGEST AND SMALLEST

numbers = [12,45,7,23,56,89,34]

largest = numbers[0]
smallest = numbers[0]

for num in numbers:
    if num > largest:
        largest = num
    if num < smallest:
        smallest = num

print("Largest:", largest)
print("Smallest:", smallest)

print ("====================================")
# PASS OR FAIL

grades = {
    "Carl": 85,
    "Anna": 90,
    "John": 95
}

for name, grade in grades.items():
    if grade >= 75:
        print(name + ": Pass")
    else:
        print(name + ": Fail")

print ("====================================")
# REVERSED WORD

def reverse_word(w):
    reverse_w = " "
    for char in w:
        reverse_w = char + reverse_w
    return reverse_w

input_str = "python"
reversed_str = reverse_word(input_str)

print("Original Word: ", input_str)
print("Reversed Word: ", reversed_str)

print ("====================================")
# EVEN NUMBERS 

nums = [3,10,7,18,21,4,6]
even_numbers = [val for val in nums if val % 2 == 0]
print(even_numbers)

print ("====================================")
# TABLE

num = int(input("Enter a number: "))

for i in range(1,11):
    print(f"{num} x {i} = {num * i}")

print ("====================================")
# DUPLICATE VALUE

numbs = [1,2,3,4,2,5,6,3,7]
seen = set()
duplicates = set()

for item in numbs:
    if item in seen:
        duplicates.add(item)
    else:
        seen.add(item)

print("Duplicate Value: ", (list(duplicates)))

print ("====================================")
# SUM OF ODD AND EVEN

numbers = [3,10,7,18,21,4,6]
even_sum = 0
odd_sum = 0

for num in numbers:
    if num % 2 == 0:
        even_sum += num
    else:
        odd_sum += num

print("Sum of even numbers:", even_sum)
print("Sum of odd numbers:", odd_sum)

print ("====================================")
# LARGE,SMALL, & DIFFERENCE

numbers1 = [12, 45, 7, 23, 56, 89, 34]
largest = numbers1[0]
smallest = numbers1[0]

for num in numbers1:
    if num > largest:
        largest = num
    if num < smallest:
        smallest = num
    
difference = largest - smallest

print("Largest:", largest)
print("Smallest:", smallest)
print("Difference:", difference)
        
print ("====================================")
# AVERAGE

numbers = [2,4,6,8]
total = sum(numbers)
count  = len(numbers)
average = total / count

print("The average of this list is: ", average)

print ("====================================")
# SECOND LARGEST

nums = [3,8,1,10,6]
unique_numbers = sorted(list(nums))
second_largest = unique_numbers[-2]

print("The second largest number is: ", second_largest)
print ("====================================")
# FREQUENCY COUNT

sentence = "ai is the future and ai is powerful"

words = sentence.split()

word_count = {}

for word in words:
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1

for word, count in word_count.items():
    print(f"{word}: {count}")

print ("====================================")
# DATASET STATISTICS ANALYZER

data = [10,20,30,40,50]

data_sum = sum(data)
total_data = len(data)
average = data_sum / total_data

print("Max Number: ", max(data))
print("Min Number: ", min(data))
print("Number Count: ", total_data)
print("Average: ", average)
print("Sum of all Number: ", data_sum)

print ("====================================")
