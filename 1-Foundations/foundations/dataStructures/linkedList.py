# LINKED LIST FULL IMPLEMENTATION


# Node class
class Node:

    def __init__(self, data):
        self.data = data
        self.next = None


# Linked List class
class LinkedList:

    def __init__(self):
        self.head = None


    # Insert at beginning
    def insert_beginning(self, value):

        new_node = Node(value)

        new_node.next = self.head
        self.head = new_node


    # Insert at end
    def insert_end(self, value):

        new_node = Node(value)

        if self.head is None:
            self.head = new_node
            return

        temp = self.head

        while temp.next:
            temp = temp.next

        temp.next = new_node


    # Traverse / display
    def display(self):

        temp = self.head

        while temp:
            print(temp.data, end=" -> ")
            temp = temp.next

        print("None")


    # Search element
    def search(self, target):

        temp = self.head

        while temp:

            if temp.data == target:
                return True

            temp = temp.next

        return False


    # Delete node
    def delete(self, key):

        temp = self.head

        if temp and temp.data == key:
            self.head = temp.next
            return

        prev = None

        while temp and temp.data != key:
            prev = temp
            temp = temp.next

        if temp is None:
            print("Value not found")
            return

        prev.next = temp.next


    # Reverse linked list
    def reverse(self):

        prev = None
        current = self.head

        while current:

            next_node = current.next
            current.next = prev

            prev = current
            current = next_node

        self.head = prev


    # Find middle node
    def find_middle(self):

        slow = self.head
        fast = self.head

        while fast and fast.next:

            slow = slow.next
            fast = fast.next.next

        return slow.data


    # Detect cycle
    def detect_cycle(self):

        slow = self.head
        fast = self.head

        while fast and fast.next:

            slow = slow.next
            fast = fast.next.next

            if slow == fast:
                return True

        return False



# TEST PROGRAM

ll = LinkedList()

ll.insert_end(10)
ll.insert_end(20)
ll.insert_end(30)
ll.insert_end(40)

print("Linked List:")
ll.display()


print("\nSearch 20:")
print(ll.search(20))


print("\nDelete 30:")
ll.delete(30)
ll.display()


print("\nReverse List:")
ll.reverse()
ll.display()


print("\nMiddle Node:")
print(ll.find_middle())


print("\nCycle Detection:")
print(ll.detect_cycle())