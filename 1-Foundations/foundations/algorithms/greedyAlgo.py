# EASY
coins = [25,10,5,1]
amount = 63

for coin in coins:
    while amount >= coin:
        print(coin)
        amount -= coin

# MEDIUM

start = [1,3,0,5,8,5]
finish = [2,4,6,7,9,9]

activities = list(zip(start, finish))

activities.sort(key=lambda x: x[1])

last_end = 0

for s,f in activities:
    if s >= last_end:
        print(s,f)
        last_end = f
    
# HARD
items = [(60,10),(100,20),(120,30)]

items.sort(key=lambda x: x[0]/x[1], reverse=True)

capacity = 50
total_value = 0

for value,weight in items:

    if capacity >= weight:
        capacity -= weight
        total_value += value

    else:
        fraction = capacity/weight
        total_value += value * fraction
        break

print(total_value)