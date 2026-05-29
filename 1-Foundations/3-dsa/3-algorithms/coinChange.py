# EASY
def fibonacci(n):

    if n <= 1:
        return n

    prev2 = 0
    prev1 = 1

    for i in range(2, n + 1):

        current = prev1 + prev2

        prev2 = prev1
        prev1 = current

    return prev1


print(fibonacci(10))

# MEDIUM
def coin_change_combination(coins, amount):

    dp = [float('inf')] * (amount + 1)
    parent = [-1] * (amount + 1)

    dp[0] = 0

    for coin in coins:
        for i in range(coin, amount + 1):

            if dp[i-coin] + 1 < dp[i]:

                dp[i] = dp[i-coin] + 1
                parent[i] = coin

    result = []

    while amount > 0:
        result.append(parent[amount])
        amount -= parent[amount]

    return result


print(coin_change_combination([1,2,5],11))

# HARD
def coin_change_ways(coins, amount):

    dp = [0] * (amount + 1)

    dp[0] = 1

    for coin in coins:
        for i in range(coin, amount + 1):

            dp[i] += dp[i-coin]

    return dp[amount]


print(coin_change_ways([1,2,5],5))