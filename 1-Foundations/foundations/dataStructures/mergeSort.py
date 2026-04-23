# EASY
def merge(arr1,arr2):

    result = []
    i=j=0

    while i<len(arr1) and j<len(arr2):

        if arr1[i] < arr2[j]:
            result.append(arr1[i])
            i+=1
        else:
            result.append(arr2[j])
            j+=1

    result.extend(arr1[i:])
    result.extend(arr2[j:])

    return result


a = [1,3,5]
b = [2,4,6]

print(merge(a,b))

# MEDIUM
def merge_sort(arr):

    if len(arr) > 1:

        mid = len(arr)//2

        left = arr[:mid]
        right = arr[mid:]

        merge_sort(left)
        merge_sort(right)

        i=j=k=0

        while i<len(left) and j<len(right):

            if left[i] < right[j]:
                arr[k]=left[i]
                i+=1
            else:
                arr[k]=right[j]
                j+=1

            k+=1

        while i<len(left):
            arr[k]=left[i]
            i+=1
            k+=1

        while j<len(right):
            arr[k]=right[j]
            j+=1
            k+=1


arr=[38,27,43,3,9,82,10]

merge_sort(arr)

print(arr)

# HARD 
def merge_count(arr):

    if len(arr) <= 1:
        return arr,0

    mid = len(arr)//2

    left,count_left = merge_count(arr[:mid])
    right,count_right = merge_count(arr[mid:])

    merged = []
    i=j=0
    count = count_left + count_right

    while i<len(left) and j<len(right):

        if left[i] <= right[j]:
            merged.append(left[i])
            i+=1
        else:
            merged.append(right[j])
            count += len(left)-i
            j+=1

    merged += left[i:]
    merged += right[j:]

    return merged,count


arr = [2,4,1,3,5]

print(merge_count(arr)[1])