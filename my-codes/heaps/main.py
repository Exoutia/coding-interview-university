def max_heapify(arr: list[int], heap_size: int, index: int):
    left = 2 * index + 1
    right = 2 * index + 2

    largest = index
    
    if left < heap_size and arr[left] > arr[index]:
        largest = left

    if right < heap_size and arr[right] > arr[largest]:
        largest = right

    if largest != index:
        arr[index], arr[largest] = arr[largest], arr[index]
        max_heapify(arr, heap_size, largest)

def build_max_heap(arr: list[int]):
    heap_size = len(arr)

    for i in range(heap_size // 2, -1, -1):
        max_heapify(arr, heap_size, i)

def heapsort(arr: list[int]):
    build_max_heap(arr)
    # print("after heapify:", arr)
    
    for end in range(len(arr) - 1, -1, -1):
        arr[end], arr[0] = arr[0], arr[end]
        # print(arr)
        max_heapify(arr, end, 0)

class EmptyException(Exception):
    pass

class PriorityQueue:

    def __init__(self, arr: list[int]) -> None:
        self._data = arr
        self._build_max_heap()

    def _build_max_heap(self):
        heap_size = len(self)
        for i in range(heap_size // 2, -1, -1):
            self._max_heapify_down(i)

    def _max_heapify_down(self, index: int) -> None:
        left, right = self._left_child_index(index), self._right_child_index(index)
        largest = index
        
        if left and self._data[left] > self._data[index]:
            largest = left

        if right and self._data[right] > self._data[largest]:
            largest = right

        if largest != index:
            self._data[index], self._data[largest] = self._data[largest], self._data[index]
            self._max_heapify_down(largest)
    
    def _parent_index(self, child_index: int) -> int:
        return (child_index - 1) // 2

    def _left_child_index(self, parent_index: int) -> int | None:
        left_child_index = 2 * parent_index + 1
        return None if left_child_index >= len(self) else left_child_index
        
    def _right_child_index(self, parent_index: int) -> int | None:
        right_child_index = 2 * parent_index + 2
        return None if right_child_index >= len(self) else right_child_index

    def _max_heapify_up(self, index: int):
        if index == 0:
            return
        parent_index = self._parent_index(index)

        if self._data[parent_index] >= self._data[index]:
            return
        else:
            self._data[parent_index], self._data[index] = self._data[index], self._data[parent_index]
            return self._max_heapify_up(parent_index)

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return len(self) == 0

    def insert(self, val: int):
        self._data.append(val)
        self._max_heapify_up(len(self) - 1)

    def pop(self):
        if self.is_empty():
            raise EmptyException("PriorityQueue is empty")
        self._data[0], self._data[-1] = self._data[-1], self._data[0]
        val = self._data.pop()
        self._max_heapify_down(0)
        return val

    def remove(self, index: int) -> int:
        if index >= len(self):
            raise IndexError("Index out of range")

        self._data[index], self._data[-1] = self._data[-1], self._data[index]
        val = self._data.pop()
        self._max_heapify_down(index)
        return val

    def largest_element(self):
        return self._data[0]

def main():
    arr = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    queue = PriorityQueue(arr)
    for i in (1, -1, -8, 100, 10083, -1, 94, -3, 0):
        queue.insert(i)
        print(queue.largest_element(), i)

    while not queue.is_empty():
        print(queue.pop())

if __name__ == "__main__":
    main()


        
