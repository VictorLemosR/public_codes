# Created from a simple list with dequeue O(n), which is not optimal
class SimpleQueue:
    def __init__(self):
        self.queue = []

    def dequeue(self):
        # This operation is O(n), which is bad for a queue
        if self.is_empty():
            return
        return self.queue.pop()

    def enqueue(self, item):
        self.queue.insert(0, item)

    def peek(self):
        if self.is_empty():
            print("Queue is empty")
            return
        return self.queue[-1]

    def is_empty(self):
        if len(self.queue) == 0:
            return True

        return False


# Define a max size for queue, pre-allocate that size for a list and keep 2 pointers.
# One pointer to the first in line and other to the last in line.
# Opposed to SimpleQueue, the list is from right to left, enqueued at end and dequeued at start
class CircularQueue:
    def __init__(self, n):
        self.queue = [None] * n
        self.head = 0
        self.tail = -1
        self.max_size = n
        self.empty = True

    def dequeue(self):
        # This operation is O(n), which is bad for a queue
        if self.empty:
            print("Queue is empty")
            return

        if self.size == 1:
            self.empty = True

        value = self.queue[self.head]
        if self.head == self.max_size - 1:
            self.head = 0
        else:
            self.head += 1

        return value

    def enqueue(self, item):
        if self.size() == self.max_size:
            print("Queue already full. No value inserted")
            return

        if self.empty:
            self.empty = False
        if self.tail == self.max_size - 1:
            self.tail = 0
        else:
            self.tail += 1

        self.queue[self.tail] = item

    def peek(self):
        if self.empty:
            print("Queue is empty")
            return
        return self.queue[self.head]

    def size(self):
        return (self.tail - self.head + 1) % self.max_size

# Queue generated with linked list
class LinkedQueue:

    def __init__(self):
        self.

q = CircularQueue(10)

q.dequeue()
q.peek()
print(q.empty)
q.enqueue(10)
print(f"->> q <<- function: Not inside a function; file: data_algorithms.py\n{q.queue}")
print(q.empty)
q.enqueue(20)
print(f"->> q <<- function: Not inside a function; file: data_algorithms.py\n{q.queue}")
print(q.peek())
q.dequeue()
print(f"->> q <<- function: Not inside a function; file: data_algorithms.py\n{q.queue}")
print(q.peek())
