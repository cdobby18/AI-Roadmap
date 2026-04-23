# EASY
stack = []

# push elements
stack.append(10)
stack.append(20)
stack.append(30)

print("Stack after pushes:", stack)

# pop element
removed = stack.pop()

print("Removed element:", removed)
print("Stack after pop:", stack)

# MEDIUM
def is_balanced(expression):

    stack = []

    for char in expression:

        if char == "(":
            stack.append(char)

        elif char == ")":
            if not stack:
                return False
            stack.pop()

    return len(stack) == 0


print(is_balanced("(())"))
print(is_balanced("(()"))

# HARD
def evaluate_postfix(expression):

    stack = []

    for char in expression:

        if char.isdigit():
            stack.append(int(char))

        else:
            b = stack.pop()
            a = stack.pop()

            if char == "+":
                stack.append(a + b)

            elif char == "-":
                stack.append(a - b)

            elif char == "*":
                stack.append(a * b)

            elif char == "/":
                stack.append(a / b)

    return stack[0]


print(evaluate_postfix("23*54*+9-"))