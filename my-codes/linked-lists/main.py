class Node:
    def __init__(self, val: int, next_node=None) -> None:
        self.val = val
        self.next = next_node

    def __str__(self):
        return f"Node({self.val}, next={self.next.val if self.next else None})"


class EmptyLinkedList(Exception):
    pass


class LinkedList:
    # TDOD: reverse() - reverses the list
    # TDOD: remove_value(value) - removes the first item in the list with this value

    def __init__(self, head: Node, tail: Node) -> None:
        self._head = head
        self._tail = tail

    @classmethod
    def list_to_linkedlist(cls, nums: list[int]):
        head = tail = Node(nums[0])
        for i in range(1, len(nums)):
            tail.next = Node(nums[i])
            tail = tail.next
        return cls(head, tail)

    def __len__(self):
        tmp = self._head
        size = 0
        while tmp:
            size += 1
            tmp = tmp.next
        return size

    def __getitem__(self, ind):
        try:
            tmp = self._head
            fast = tmp.next
            for _ in range(ind):
                tmp = tmp.next
                fast = fast.next
            return tmp
        except AttributeError:
            raise IndexError("Out of bounds")

    def is_empty(self):
        if self._head is None:
            return True
        return False

    def push_front(self, node: Node):

        self._head, node.next = node, self._head

    def pop_front(self) -> Node:
        try:
            self._head, tmp = self._head.next, self._head
            tmp.next = None
            return tmp
        except AttributeError:
            raise EmptyLinkedList("List is empty")

    def push_back(self, node: Node):
        self._tail.next, self._tail = node, node

    def value_n_from_end(self, ind):
        try:
            fast = self._head
            for _ in range(ind - 1):
                fast = fast.next
            tmp = self._head
            while fast.next:
                tmp = tmp.next
                fast = fast.next
            return tmp
        except Exception:
            raise IndexError("Index out of range")

    @property
    def front(self):
        return self._head

    @property
    def back(self):
        return self._tail

    def pop_back(self):
        try:
            tmp = self._head
            while tmp.next.next:
                tmp = tmp.next

            tmp.next = None
            back = self._tail
            self._tail = tmp

            return back
        except Exception:
            raise EmptyLinkedList("List is empty")

    def insert(self, ind, val):
        if ind == 0:
            self.push_front(val)
        try:
            prev = self._head
            for _ in range(ind - 1):
                prev = prev.next
            nex = prev.next
            prev.next = Node(val)

            prev.next.next = nex

        except Exception:
            raise IndexError("Index out of range")

    def erase(self, ind):
        if ind == 0:
            self.pop_front()
        try:
            prev = self._head
            for _ in range(ind - 1):
                prev = prev.next
            nex_next = prev.next.next
            prev.next = nex_next
        except Exception:
            raise IndexError("Invalid index")

    def reverse(self):
        cur = self._head
        prev = None
        while cur:
            nex = cur.next
            cur.next = prev
            prev = cur
            cur = nex
        self._tail = self._head
        self._head = prev

    def __str__(self):
        tmp = self._head
        res = []
        while tmp:
            res.append(str(tmp.val))
            tmp = tmp.next
        return " -> ".join(res)

    def remove_value(self, val):
        tmp = slow = Node(-1)
        cur = slow.next = self._head
        while cur:
            if cur.val == val:
                slow.next = slow.next.next
                break
            cur = cur.next
            slow = slow.next
        self._head = tmp.next

            


if __name__ == "__main__":
    head = LinkedList.list_to_linkedlist([0, 1, 2, 3, 4, 5])
    print(head)
    head.insert(6, 8)
    print(head)
    for i in range(1, 8):
        print(head.value_n_from_end(i))
    print(head, head.front, head.back, sep=" | ")

    repeat = LinkedList.list_to_linkedlist([0, 0, 0, 0, 3, 4, 4, 5])
    print(repeat)
    repeat.remove_value(-1)
    print(repeat)
