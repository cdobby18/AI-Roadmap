# EASY
numbers = [4, 9, 2, 7, 5]

max_num = numbers[0]

for num in numbers:
    if num > max_num:
        max_num = num

print(max_num)

# MEDIUM
nums = [2,7,11,15]
target = 9

for i in range(len(nums)):
    for j in range(i+1, len(nums)):
        if nums[i] + nums[j] == target:
            print(i, j)

# HARD
from itertools import permutations

string = "ABC"

perm = permutations(string)

for p in perm:
    print("".join(p))