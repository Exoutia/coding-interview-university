from sys import setprofile
from typing import Self


class Node:
    def __init__(self, val: int, next_node=None) -> None:
        self.val = val
        self.next = next_node

    def __str__(self):
        return f"Node({self.val}, next={self.next.val if self.next else None})"


class EmptyQueueError(Exception):
    pass


class QueueLinkedList:
    def __init__(self):
        self._tail = self._head = Node(0)

    def enqueue(self, val: int):
        self._tail.next = Node(val)
        self._tail = self._tail.next

    def dequeue(self):
        if self._head.next == self._tail:
            self._tail = self._head

        tmp = self._head.next
        self._head.next = tmp.next
        res = tmp.val
        return res

    def is_empty(self):
        return self._head == self._tail

    @property
    def front(self):
        if self.is_empty():
            return None
        return self._head.next.val

    @property
    def back(self):
        if self.is_empty():
            return None
        return self._tail.val

    def __str__(self):
        tmp = self._head.next
        res = []
        while tmp:
            res.append(str(tmp.val))
            tmp = tmp.next
        return " -> ".join(res) + f" | head: {self.front} | tail: {self.back}"


if __name__ == "__main__":
    q = QueueLinkedList()

    for i in range(9):
        q.enqueue(i)
    for _ in range(9):
        print(q.back, q.front)
        q.dequeue()

    for i in range(9, -1, -1):
        q.enqueue(i)
    print(q)
