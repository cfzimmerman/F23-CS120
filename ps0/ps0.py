#################
#               #
# Problem Set 0 #
#               #
#################

from typing import Optional

#
# Setup
#


class BinaryTree:
    def __init__(self, root):
        self.root: BTvertex = root


class BTvertex:
    def __init__(self, key):
        self.parent: BTvertex = None
        self.left: BTvertex = None
        self.right: BTvertex = None
        self.key: int = key
        self.size: int = None


#
# Problem 1a
#

# Input: BTvertex v, the root of a BinaryTree of size n
# Output: Up to you
# Side effect: sets the size of each vertex n in the
# ... tree rooted at vertex v to the size of that subtree
# Runtime: O(n)


def calculate_sizes(v: Optional[BTvertex]) -> int:
    if v is None:
        return 0
    left = calculate_sizes(v.left)
    right = calculate_sizes(v.right)
    v.size = left + right + 1
    return v.size


#
# Problem 1c
#

# Input: BTvertex r, the root of a size-augmented BinaryTree T
# ... of size n and height h
# Output: A BTvertex that, if removed from the tree, would result
# ... in disjoint trees that all have at most n/2 vertices
# Runtime: O(h)


def find_vertex(r: Optional[BTvertex]) -> Optional[BTvertex]:
    if r is None:
        return r
    half = r.size // 2
    while r:
        if r.left and r.left.size > half:
            r = r.left
            continue
        if r.right and r.right.size > half:
            r = r.right
            continue
        return r
    raise Exception("failed to find a solution")
