class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Deque:
    def __init__(self):
        self.front_node = None
        self.rear_node = None
        self._size = 0

    def is_empty(self):
        return self._size == 0

    def size(self):
        return self._size

    def add_front(self, data):
        node = Node(data)
        node.next = self.front_node
        if self.front_node is None:
            self.rear_node = node
        self.front_node = node
        self._size += 1

    def add_rear(self, data):
        node = Node(data)
        if self.rear_node is None:
            self.front_node = node
        else:
            self.rear_node.next = node
        self.rear_node = node
        self._size += 1

    def remove_front(self):
        if self.front_node is None:
            return None

        data = self.front_node.data
        self.front_node = self.front_node.next
        if self.front_node is None:
            self.rear_node = None
        self._size -= 1
        return data

    def remove_rear(self):
        if self.front_node is None:
            return None

        data = self.rear_node.data
        if self.front_node is self.rear_node:
            self.front_node = None
            self.rear_node = None
        else:
            node = self.front_node
            while node.next is not self.rear_node:
                node = node.next
            self.rear_node = node
            self.rear_node.next = None
        self._size -= 1
        return data

    def peek_front(self):
        return None if self.front_node is None else self.front_node.data

    def peek_rear(self):
        return None if self.rear_node is None else self.rear_node.data

    def to_list(self):
        values = []
        node = self.front_node
        while node is not None:
            values.append(node.data)
            node = node.next
        return values


class Queue:
    def __init__(self):
        self._items = Deque()

    def enqueue(self, data):
        self._items.add_rear(data)

    def dequeue(self):
        return self._items.remove_front()

    def front(self):
        return self._items.peek_front()

    def rear(self):
        return self._items.peek_rear()

    def is_empty(self):
        return self._items.is_empty()

    def size(self):
        return self._items.size()

    def to_list(self):
        return self._items.to_list()
