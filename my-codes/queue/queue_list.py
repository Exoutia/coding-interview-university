from array import array
from enum import Enum


class TypeCode(Enum):
    INTEGER = "i"
    FLOAT = "d"


class Empty(Exception):
    pass


class QueueList:

    CAPACITY = 10

    def __init__(self, typecode: TypeCode = TypeCode.INTEGER) -> None:
        self._front = 0
        self._size = 0
        self._typecode = typecode
        self._data = array(typecode.value, [0] * QueueList.CAPACITY)

    def _resize(self, cap: int):
        old = self._data
        self._data = array(self._typecode.value, [0] * cap)
        walk = self._front
        for k in range(self._size):
            self._data[k] = old[walk]
            walk = (1 + walk) % len(old)
        self._front = 0

    def enqueue(self, val):
        if len(self._data) == self._size:
            self._resize(2 * len(self._data))
        avail = (self._front + self._size) % len(self._data)
        self._data[avail] = val
        self._size += 1

    def is_empty(self):
        return self._size == 0

    def dequeue(self):
        if self.is_empty():
            raise Empty("Queue is empty")
        ans = self._data[self._front]
        self._front = (self._front + 1) % len(self._data)
        self._size -= 1
        return ans

    def __str__(self):
        return str(self._data)


if __name__ == "__main__":
    q = QueueList()
    for i in range(9):
        q.enqueue(i)

    for i in range(3):
        print(q.dequeue())

    for i in range(9):
        q.enqueue(i)
    print(q)
