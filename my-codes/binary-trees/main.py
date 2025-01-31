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


class BST:
    def __init__(self, root: Node | None) -> None:
        self.root = root

    @classmethod
    def list_to_tree(cls, nums: list[int]):
        nums.sort()
        def make(nums: list[int]):
            if nums:
                root_ind = len(nums) // 2
                root_node = Node(nums[root_ind])
                root_node.left = make(nums[:root_ind])
                root_node.right = make(nums[root_ind + 1:])
                return root_node
        return cls(make(nums))

    def insert_iterative(self, element: int):
        node = self.root
        while node:
            upper = node
            if node.val > element:
                node = node.left
            else:
                node = node.right
        if upper.val > element:
            upper.left = Node(element)
        else:
            upper.right = Node(element)

    def insert(self, element: int):
        def helper(node, val):
            if not node:
                return Node(val)
            if node.val > val:
                node.left = helper(node.left, val)
            else:
                node.right = helper(node.right, val)
            return node
        self.root = helper(self.root, element)

    def delete_tree_without_deleting_root(self): 
        
        def helper(node):
            if node:
                helper(node.left)
                helper(node.right)
                del node
            return None
        return None
        

    def get_successor(self, val: int):
        def helper(node, val):
            if node is None:
                return None
            if node.val == val:
                return self._get_successor(node)
            elif node.val < val:
                return helper(node.right, val)
            else:
                return helper(node.left, val)
        ans = helper(self.root, val)
        return ans.val if ans else -1

    @staticmethod
    def _get_successor(node: Node):
        node = node.right
        while node is not None and node.left is not None:
            node = node.left
        return node

    def delete(self, element: int): 
        def helper(node, val):
            if node is None:
                return node
        
            if node.val > val:
                node.left = helper(node.left, val)
            elif node.val < val:
                node.right = helper(node.right, val)
            else:
                if node.left is None:
                    return node.right
            
                if node.right is None:
                    return node.left
                
                succ = self._get_successor(node)
                node.val = succ.val
                node.right = helper(node.right, succ.val)

            return node
        self.root = helper(self.root, element)
        
    def node_count_basic(self):
        def dfs(node, ans):
            if not node:
                return 0
            if node.left:
                ans = dfs(node.left, ans + 1)
            if node.right:
                ans = dfs(node.right, ans+1)
            return ans
        return dfs(self.root, 1) 

    def inorder(self):
        res = []
        def helper(node):
            if node:
                helper(node.left)
                res.append(node.val)
                helper(node.right)
        helper(self.root)
        return res

    def get_min(self):
        def helper(node):
            if node and node.left is None:
                return node.val
            return helper(node.left)
        return helper(self.root)
            

    def get_max(self):
        def helper(node):
            if node and node.right is None:
                return node.val
            return helper(node.right)
        return helper(self.root)
            

    @staticmethod
    def _find(node, val):
        if node is None:
            return False
        if node.val == val:
            return True
        elif node.val > val:
            return BST._find(node.left, val)
        else:
            return BST._find(node.right, val)


    def __contains__(self, val: int):
        return self._find(self.root, val)

    def get_height(self):
        def helper(node):
            if node is None:
                return 0
            return 1 + max(helper(node.left), helper(node.right))
        return helper(self.root) 

    def __str__(self) -> str:
        res = []
        q = deque([self.root])
        while q:
            lis = []
            for _ in range(len(q)):
                node = q.popleft()
                lis.append(str(node))
                if node:
                    q.append(node.left)
                    q.append(node.right)
            res.append(' | '.join(lis))
        return '\n'.join(res)


def is_binary_search_tree(root: Node) -> bool:
    def check(node):
        if node is None:
            return True
        ans = True
        if node.right:
            ans |= node.val <= node.right.val
        if node.left:
            ans |= node.val > node.left.val
        return ans and check(node.left) and check(node.right)
    return check(root)



if __name__ == "__main__":
    list_of_numbers_in_seq = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    tree = BST.list_to_tree(list_of_numbers_in_seq)
    print(tree.get_successor(0))
