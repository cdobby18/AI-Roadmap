# EASY
arr = [10, 20, 30]
x = arr.pop()  # removes last element
print(x)       # 30
print(arr)     # [10, 20]

# MEDIUM
arr1 = [10, 20, 30, 40]
y = arr1.pop(1)  # removes element at index 1
print(y)        # 20
print(arr1)      # [10, 30, 40]

# HARD
arr = [5, 3, 8, 2, 7]
i = 0
while i < len(arr):
    if arr[i] % 2 == 0:
        arr.pop(i)
    else:
        i += 1
print(arr)  # [5, 3, 7]