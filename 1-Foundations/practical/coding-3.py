print("====================================")
# STACK - reverse string 
# 1.) python -> nothyp

def reverse_string(s):
    stack = []

    for char in s:
        stack.append(char)

    reversed_str = ""

    while stack:
        reversed_str += stack.pop()

    return reversed_str

input_str = "python"
output_str = reverse_string(input_str)
print("Origina String: ", input_str)
print("Reversed: String: ", output_str)

# 2.) Balanced Parenthesis

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

print(is_balanced("((())())"))
print(is_balanced("(()))("))

# 3. Stack Class OOP

class Stack():
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            return None
        
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            return None
        
    def is_empty(self):
        return(len(self.items)) == 0
    
original_list = [1,2,3,4,5]
stack = Stack()

for num in original_list:
    stack.push(num)

reversed_list = []
while not stack.is_empty():
    reversed_list.append(stack.pop())

print("Original List: ", original_list)
print("Reversed List: ", reversed_list)

# 4.) Balanced Parenthesis Advanced
def is_balanced(expression):
    stack = []
    pairs = {')':'(', '}':'{', ']':'['}

    for char in expression:
        if char in "({[":
            stack.append(char)
        elif char in ")}]":
            if not stack or stack[-1] != pairs[char]:
                return False
            stack.pop()

    return len(stack) == 0

print(is_balanced("{[()()]}"))   
print(is_balanced("{[(])}"))    
print(is_balanced("({[]})"))   
print(is_balanced("([)]"))       
print(is_balanced("{[()]}"))     