# EASY
def knapsack(weights, values, capacity):

    n = len(weights)

    dp = [[0]*(capacity+1) for _ in range(n+1)]

    for i in range(1,n+1):

        for w in range(capacity+1):

            if weights[i-1] <= w:

                dp[i][w] = max(
                    values[i-1] + dp[i-1][w-weights[i-1]],
                    dp[i-1][w]
                )

            else:
                dp[i][w] = dp[i-1][w]

    return dp[n][capacity]


print(knapsack([2,3,4],[4,5,6],5))

# MEDIUM
def knapsack_optimized(weights, values, capacity):

    dp = [0]*(capacity+1)

    for i in range(len(weights)):

        for w in range(capacity, weights[i]-1, -1):

            dp[w] = max(dp[w], values[i] + dp[w-weights[i]])

    return dp[capacity]


print(knapsack_optimized([2,3,4],[4,5,6],5))

# HARD
def knapsack_items(weights, values, capacity):

    n = len(weights)

    dp = [[0]*(capacity+1) for _ in range(n+1)]

    for i in range(1,n+1):

        for w in range(capacity+1):

            if weights[i-1] <= w:

                dp[i][w] = max(values[i-1] + dp[i-1][w-weights[i-1]], dp[i-1][w])

            else:
                dp[i][w] = dp[i-1][w]

    w = capacity
    items = []

    for i in range(n,0,-1):

        if dp[i][w] != dp[i-1][w]:

            items.append(i-1)
            w -= weights[i-1]

    return items


print(knapsack_items([2,3,4],[4,5,6],5))