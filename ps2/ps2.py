from __future__ import annotations
from collections import deque


class BinarySearchTree:
    # left: BinarySearchTree
    # right: BinarySearchTree
    # key: int
    # item: int
    # size: int
    def __init__(self, debugger=None):
        self.left: BinarySearchTree | None = None
        self.right: BinarySearchTree | None = None
        self.key: int | None = None
        self.item: BinarySearchTree | None = None
        self._size: int = 1
        self.debugger = debugger

    @property
    def size(self) -> int:
        return self._size

    # a setter function
    @size.setter
    def size(self, a):
        debugger = self.debugger
        if debugger:
            debugger.inc_size_counter()
        self._size = a

    # Part a

    def calculate_sizes(self, debugger=None):
        """
        Calculates the size of the tree
        returns the size at a given node
        """
        # Debugging code
        # No need to modify
        # Provides counts
        if debugger is None:
            debugger = self.debugger
        if debugger:
            debugger.inc()

        # Implementation
        self.size = 1
        if self.right is not None:
            self.size += self.right.calculate_sizes(debugger)
        if self.left is not None:
            self.size += self.left.calculate_sizes(debugger)
        return self.size

    def select(self, ind: int) -> BinarySearchTree | None:
        """
        Select the ind-th key in the tree
        ind: a number between 0 and n-1 (the number of nodes/objects)
        returns BinarySearchTree/Node or None
        """
        left_size = 0
        if self.left is not None:
            left_size = self.left.size
        if ind == left_size:
            return self
        if left_size > ind and self.left is not None:
            return self.left.select(ind)
        if left_size < ind and self.right is not None:
            return self.right.select(ind - left_size - 1)
        # ^ Fix here, explained in PDF
        return None

    def search(self, key: int) -> BinarySearchTree | None:
        """
        Searches for a given key
        returns a pointer to the object with target key or None (Roughgarden)
        """
        if self is None:
            return None
        elif self.key == key:
            return self
        elif self.key < key and self.right is not None:
            return self.right.search(key)
        elif self.left is not None:
            return self.left.search(key)
        return None

    def insert(self, key: int) -> BinarySearchTree | None:
        """
        Inserts a key into the tree
        key: the key for the new node;
            ... this is NOT a BinarySearchTree/Node, the function creates one

        returns the original (top level) tree - allows for easy chaining in
        tests
        """
        if self.key is None:
            self.key = key
        elif self.key > key:
            if self.left is None:
                self.left = BinarySearchTree(self.debugger)
            self.left.insert(key)
            self.size += 1
            # ^ added
        elif self.key < key:
            if self.right is None:
                self.right = BinarySearchTree(self.debugger)
            self.right.insert(key)
            self.size += 1
            # ^ added
        # self.calculate_sizes()
        # ^ removed
        return self

    # Part b

    def __recalc_size(self) -> int:
        """returns the size of a subtree rooted at self as derived from the
        sizes of the children of the root node"""
        sum = 0
        if self.left:
            sum += self.left.size
        if self.right:
            sum += self.right.size
        return sum

    def __rotate_left(self) -> BinarySearchTree:
        """Performs leftward tree rotation. Assumes a right node exists. That
        right node will be returned as the new subtree root."""
        prev_n_right = self.right
        assert prev_n_right is not None

        # redirect pointers
        self.right = self.right.left
        prev_n_right.left = self

        # recalculate sizes
        self.size = self.__recalc_size()
        prev_n_right.size = prev_n_right.__recalc_size()

        return prev_n_right

    def __rotate_right(self) -> BinarySearchTree:
        """Performs rightward tree rotation. Assumes a left node exists. That
        left node will be returned as the new subtree root."""
        prev_n_left = self.left
        assert prev_n_left is not None

        # redirect pointers
        self.left = self.left.right
        prev_n_left.right = self

        # recalculate sizes
        self.size = self.__recalc_size()
        prev_n_left.size = prev_n_left.__recalc_size()

        return prev_n_left

    def rotate(self, direction, child_side):
        """
        Performs a `direction`-rotate the `side`-child of (the root of) T (self)
        direction: "L" or "R" to indicate the rotation direction
        child_side: "L" or "R" which child of T to perform the rotate on
        Returns: the root of the tree/subtree
        Example:
        Original Graph
          10
           \
            11
              \
               12

        Execute: NodeFor10.rotate("L", "R") -> Outputs: NodeFor10
        Output Graph
          10
            \
            12
            /
           11
        """
        assert child_side == "L" or child_side == "R"
        assert direction == "L" or direction == "R"

        if child_side == "L":
            if direction == "L":
                self.left = self.left.__rotate_left()
            else:
                self.left = self.left.__rotate_right()
        else:
            if direction == "L":
                self.right = self.right.__rotate_left()
            else:
                self.right = self.right.__rotate_right()
        if self.size != self.calculate_sizes():
            self.print_bst_bfs()
        return self

    def print_bst_bfs(self):
        pending = deque()
        pending.appendleft(self)
        while len(pending) > 0:
            layerLen = len(pending)
            row = []
            for _ in range(0, layerLen):
                next = pending.pop()
                row.append(f"{next.key}: {next.size}")
                if next.left:
                    pending.appendleft(next.left)
                if next.right:
                    pending.appendleft(next.right)
            print(row)

    def print_bst(self):
        if self.left is not None:
            self.left.print_bst()
        print(f"{self.key}: {self.size}"),
        if self.right is not None:
            self.right.print_bst()
        return self
