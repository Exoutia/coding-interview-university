from collections import deque
from typing import Self


class Node:
    def __init__(
        self, val: int, right: Self | None = None, left: Self | None = None
    ) -> None:
        self.val = val
        self.right = right
        self.left = left


    def __repr__(self):
        return str(self)
    def __str__(self):
        return f"node={self.val}"


class Tree:
    def __init__(self, root: Node | None) -> None:
        self.root = root

    @classmethod
    def list_to_tree(cls, nums: list[int]):
        def make(nums: list[int]):
            if nums:
                root_ind = len(nums) // 2
                root_node = Node(nums[root_ind])
                root_node.left = make(nums[:root_ind])
                root_node.right = make(nums[root_ind + 1:])
                return root_node
        return Tree(make(nums))
    
    def inorder_print(self):
        res = []
        def helper_print(node=self.root):
            if node is None:
                return
            helper_print(node.left)
            res.append(node.val)
            helper_print(node.right)
        helper_print()
        return res

    def postorder_print(self):
        res = []
        def helper_print(node=self.root):
            if node is None:
                return
            helper_print(node.left)
            helper_print(node.right)
            res.append(node.val)
        helper_print()
        return res

    def preorder_print(self):
        res = []
        def helper_print(node=self.root):
            if node is None:
                return
            res.append(node.val)
            helper_print(node.left)
            helper_print(node.right)
        helper_print()
        return res

    def bfs(self):
        res = []
        q = deque([self.root])
        while q:
            for _ in range(len(q)):
                node = q.popleft()
                if node:
                    res.append(node.val)
                    q.append(node.left)
                    q.append(node.right)
        return res
    
    def dfs(self):
        res = []
        stack = []
        visited = {}
        pass


if __name__ == "__main__":
    x = Tree.list_to_tree([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print(x.bfs())
    print(x.inorder_print())
    print(x.postorder_print())
    print(x.preorder_print())
