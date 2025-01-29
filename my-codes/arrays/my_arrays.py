class Vec:
    def __init__(self) -> None:
        self._capacity = 16
        self._size = 0
        self.data = [None] * self._capacity

    def __len__(self):
        return self._size

    def _resize(self):
        tmp_arr = self.data
        self.data = [None] * self._capacity
        for i in range(len(self)):
            self.data[i] = tmp_arr[i]

    def _extend_data_capacity(self):
        self._capacity = self._capacity << 1
        self._resize()

    def _reduce_data_capacity(self):
        self._capacity = self._capacity >> 1
        self._resize()

    def append(self, ele):
        if self._capacity == self._size:
            self._extend_data_capacity()
        self.data[self._size] = ele
        self._size += 1

    def __setitem__(self, index: int, val):
        if index >= len(self):
            raise IndexError("Index is out of bound")
        self.data[index] = val

    def __getitem__(self, index):
        if index >= len(self):
            raise IndexError("Index is out of bound")
        return self.data[index]

    def pop(self):
        tmp, self.data[len(self)] = self.data[len(self)], None
        self._size -= 1
        if self._size < self._capacity // 4:
            self._reduce_data_capacity()
        return tmp

    def prepend(self, ele):
        self.insert(0, ele)

    def is_empty(self):
        return len(self) == 0

    def capacity(self):
        return self._capacity

    def insert(self, ind, ele):
        if not (len(self) >= ind >= 0):
            raise IndexError("index out of range")

        if len(self) == ind or (ind == 0 and len(self) == 0):
            return self.append(ele)

        if len(self) == self.capacity():
            self._extend_data_capacity()

        for i in range(len(self), ind, -1):
            self.data[i] = self.data[i - 1]
        self.data[ind] = ele
        self._size += 1

    def delete(self, ind):
        if not (0 <= ind < len(self)):
            raise IndexError("Out of bound error")

        for i in range(ind, len(self)):
            self.data[i] = self.data[i + 1]
        self._size -= 1

        if len(self) < self.capacity() // 4:
            self._reduce_data_capacity()

    def __iter__(self):
        return iter(self.data[: len(self)])

    def find(self, ele):
        for i, val in enumerate(self):
            if val == ele:
                return i
        return -1

    def remove(self):
        pass

    def __str__(self) -> str:
        return f"Vec([{','.join(map(str, self.data[:self._size]))}], {self._capacity})"

    def __repr__(self) -> str:

        return f"Vec([{','.join(map(str, self.data[:self._size]))}], capacity={self._capacity}, size={len(self)})"


if __name__ == "__main__":
    vec = Vec()
    cap = {}
    for i in range(1, 10):
        vec.prepend(i)
        print(vec)
    for i in vec:
        print(i)
