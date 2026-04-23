# EASY
class Node:

    def __init__(self,value):
        self.value = value
        self.left = None
        self.right = None


def insert(root,value):

    if root is None:
        return Node(value)

    if value < root.value:
        root.left = insert(root.left,value)
    else:
        root.right = insert(root.right,value)

    return root


root = None

values = [50,30,70,20,40]

for v in values:
    root = insert(root,v)

# MEDIUM
def search(root,target):

    if root is None:
        return False

    if root.value == target:
        return True

    if target < root.value:
        return search(root.left,target)
    else:
        return search(root.right,target)


print(search(root,40))
print(search(root,100))

# HARD
def inorder(root):

    if root:
        inorder(root.left)
        print(root.value)
        inorder(root.right)


inorder(root)