# EASY
arr = [64,25,12,22,11]

for i in range(len(arr)):

    min_index = i

    for j in range(i+1,len(arr)):

        if arr[j] < arr[min_index]:
            min_index = j

    arr[i],arr[min_index] = arr[min_index],arr[i]

print(arr)

# MEDIUM
def selection_sort_desc(arr):

    n = len(arr)

    for i in range(n):

        max_index = i

        for j in range(i+1,n):

            if arr[j] > arr[max_index]:
                max_index = j

        arr[i],arr[max_index] = arr[max_index],arr[i]

    return arr


arr = [4,7,1,3,9]

print(selection_sort_desc(arr))

# HARD
def kth_smallest(arr,k):

    for i in range(k):

        min_index = i

        for j in range(i+1,len(arr)):

            if arr[j] < arr[min_index]:
                min_index = j

        arr[i],arr[min_index] = arr[min_index],arr[i]

    return arr[k-1]


arr = [7,10,4,3,20,15]

print(kth_smallest(arr,3))