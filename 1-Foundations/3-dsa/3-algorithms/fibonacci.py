# EASY

def fibonacci(n):
    if n <= 1:
        return n

    dp = [0] * (n + 1)

    dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]

    return dp[n]


print(fibonacci(10))

# MEDIUM

memo = {}

def fibonacci(n):

    if n in memo:
        return memo[n]

    if n <= 1:
        return n

    memo[n] = fibonacci(n-1) + fibonacci(n-2)

    return memo[n]


print(fibonacci(10))

# HARD
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