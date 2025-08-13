# Simplest linked list
class SimpleLinkedList:
    def __init__(self):
        self.head = None

    def pop(self):
        if self.is_empty():
            print("Linked list is empty")
            return

        current_node = self.head
        next_node = self.head.next

        # Check for size 1 case
        if next_node is None:
            value = self.head.value
            self.head = None
            return value

        while next_node.next is not None:
            current_node = next_node
            next_node = current_node.next_node

        current_node.next = None

        return next_node.value

    def append(self, value):
        new_node = SimpleNode(value)
        if self.is_empty():
            self.head = new_node
        else:
            current_node = self.head
            next_node = self.head.next
            while next_node is not None:
                current_node = next_node
                next_node = next_node.next

            current_node.next = new_node

    def preappend(self, value):
        new_head = SimpleNode(value)
        new_head.next = self.head
        self.head = new_head

    def is_empty(self):
        if self.head is None:
            return True

        return False

    def __str__(self):
        if self.is_empty():
            return "[]"

        current = self.head
        print_text = "["
        while current is not None:
            print_text += str(current.value) + "->"
            current = current.next

        print_text = print_text[:-2] + "]"

        return print_text


class SimpleNode:
    def __init__(self, value):
        self.value = value
        self.next = None


# Doubly linked list: A more complete linked list with the next and previous node
class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def pop(self):
        if self.is_empty():
            print("Linked list is already empty")
            return

        value = self.tail.value
        second_to_last = self.tail.previous
        second_to_last.next = None
        self.tail = second_to_last

        return value

    def append(self, value):
        new_node = DoublyNode(value)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            return

        self.tail.next = new_node
        new_node.previous = self.tail
        self.tail = new_node

    def preappend(self, value):
        new_node = DoublyNode(value)
        if self.is_empty():
            self.head = new_node
            return

        new_node.next = self.head
        self.head.previous = new_node
        self.head = new_node

    def is_empty(self):
        if self.head is None:
            return True

        return False

    def __str__(self):
        if self.is_empty():
            return "[]"

        current = self.head
        print_text = "["
        while current is not None:
            print_text += str(current.value) + "->"
            current = current.next

        print_text = print_text[:-2] + "]"

        return print_text



class DoublyNode:
    def __init__(self, value):
        self.value = value
        self.previous = None
        self.next = None


if __name__ == "__main__":
    l = DoublyLinkedList()

    print(l.is_empty())
    l.append(19)
    print(f"->> l <<- function: __init__; file: linked_list.py\n{l}")
    l.append(5)
    print(f"->> l <<- function: __init__; file: linked_list.py\n{l}")
    print(l.is_empty())
    print(l.pop())
    print(f"->> l <<- function: __init__; file: linked_list.py\n{l}")
    l.preappend(1)
    print(f"->> l <<- function: __init__; file: linked_list.py\n{l}")


