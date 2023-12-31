from itertools import product, combinations
from time import time
from collections import deque
from typing import Set
from ps5_helpers import generate_random_graph

"""
Before you start: Read the README and the Graph implementation below.
"""


class Graph:
    """
    A graph data structure with number of nodes N, list of sets of edges, and a list of color labels.

    Nodes and colors are both 0-indexed.
    For a given node u, its edges are located at self.edges[u] and its color is self.color[u].
    """

    # Initializes the number of nodes, sets of edges for each node, and colors
    def __init__(self, N, edges=None, colors=None):
        self.N = N
        self.edges = (
            [set(lst) for lst in edges]
            if edges is not None
            else [set() for _ in range(N)]
        )
        self.colors = (
            [c for c in colors] if colors is not None else [None for _ in range(N)]
        )

    # Adds a node to the end of the list
    # Returns resulting graph
    def add_node(self):
        self.N += 1
        self.edges.append(set())
        return self

    # Adds an undirected edge from u to v
    # Returns resulting graph
    def add_edge(self, u, v):
        assert v not in self.edges[u]
        assert u not in self.edges[v]
        self.edges[u].add(v)
        self.edges[v].add(u)
        return self

    # Removes the undirected edge from u to v
    # Returns resulting graph
    def remove_edge(self, u, v):
        assert v in self.edges[u]
        assert u in self.edges[v]
        self.edges[u].remove(v)
        self.edges[v].remove(u)
        return self

    # Resets all colors to None
    # Returns resulting graph
    def reset_colors(self):
        self.colors = [None for _ in range(self.N)]
        return self

    def clone(self):
        return Graph(self.N, self.edges, self.colors)

    def clone_and_merge(self, g2, g1u, g2v):
        """
        DOES NOT COPY COLORS
        """
        g1 = self
        edges = g1.edges + [[v + g1.N for v in u_list] for u_list in g2.edges]
        g = Graph(g1.N + g2.N, edges)
        if g1u is not None and g2v is not None:
            g = g.add_edge(g1u, g2v + g1.N)
        return g

    # Checks all colors
    def is_graph_coloring_valid(self):
        for u in range(self.N):
            for v in self.edges[u]:
                # Check if every one has a coloring
                if self.colors[u] is None or self.colors[v] is None:
                    return False

                # Make sure colors on each edge are different
                if self.colors[u] == self.colors[v]:
                    return False

        return True


"""
    Introduction: We've implemented exhaustive search for you below.

    You don't need to implement any extra code for this part.
"""

# Given an instance of the Graph class G, exhaustively search for a k-coloring
# Returns the coloring list if one exists, None otherwise.


def exhaustive_search_coloring(G, k=3):
    # Iterate through every possible coloring of nodes
    for coloring in product(range(0, k), repeat=G.N):
        G.colors = list(coloring)
        if G.is_graph_coloring_valid():
            return G.colors

    # If no valid coloring found, reset colors and return None
    G.reset_colors()
    return None


"""
    Part A: Implement two coloring via breadth-first search.

    Hint: You will need to adapt the given BFS pseudocode so that it works on all graphs,
    regardless of whether they are connected.

    When you're finished, check your work by running python3 -m ps5_color_tests 2.
"""

# Given an instance of the Graph class G and a subset of precolored nodes,
# Assigns precolored nodes to have color 2, and attempts to color the rest using colors 0 and 1.
# Precondition: Assumes that the precolored_nodes form an independent set.
# If successful, modifies G.colors and returns the coloring.
# If no coloring is possible, resets all of G's colors to None and returns None.


def bfs_2_coloring(G, precolored_nodes=None):
    precolored = set() if precolored_nodes is None else precolored_nodes
    preset_color = 2

    unvisited = set(range(G.N)).difference(precolored)
    for node in precolored:
        G.colors[node] = preset_color

    if len(precolored) == G.N:
        return G.colors

    queue = deque()
    # ensures disconnected parts of the graph are visited
    while len(unvisited) > 0:
        queue.clear()
        queue.appendleft(unvisited.pop())
        curr_color = 0
        # should visit every new node connected to the first node in queue
        while len(queue) > 0:
            # bfs the current stage
            for _ in range(len(queue)):
                nxt = queue.pop()
                G.colors[nxt] = curr_color
                for neighbor in G.edges[nxt]:
                    if neighbor in unvisited:
                        queue.appendleft(neighbor)
                        unvisited.remove(neighbor)
                        continue
                    if G.colors[neighbor] == G.colors[nxt]:
                        G.reset_colors()
                        return None

            curr_color = (curr_color + 1) % 2

    return G.colors


"""
    Part B: Implement is_independent_set.
"""

# Given an instance of the Graph class G and a subset of precolored nodes,
# Checks if subset is an independent set in G


def is_independent_set(G: Graph, subset: Set[int]):
    for node in subset:
        if len(G.edges[node].intersection(subset)) > 0:
            return False
    return True


"""
    Part C: Implement the 3-coloring algorithm from the sender receiver exercise.
    
    Make sure to call the bfs_2_coloring and is_independent_set functions that you already implemented!

    Hint 1: You will want to use the Python `combinations` function from the itertools library
    to enumerate all possible independent sets. Remember that each element of combinations is a tuple,
    so you may need to convert it to a list.

    Hint 2: Python itertools functions compute their results lazily, which means that they only
    calculate each element as the program requests it. This saves time and space, since it
    doesn't need to store the entire list of combinations up front. You should NOT try to convert the result
    of the entire combinations call to a list, since that will force Python to precompute everything.
    Instead, you should iterate over them in a for loop, which will maintain the lazy behavior we want.
    See the call to "product" in exhaustive_search for an example.

    When you're finished, check your work by running python3 -m ps5_color_tests 3.
    Don't worry if some of your tests time out: that is expected.
"""

# Given an instance of the Graph class G (which has a subset of precolored nodes), searches for a 3 coloring
# If successful, modifies G.colors and returns the coloring.
# If no coloring is possible, resets all of G's colors to None and returns None.


def iset_bfs_3_coloring(G: Graph):
    for comb_len in range(0, G.N // 3 + 1):
        for comb in combinations(range(G.N), comb_len):
            comb_as_set = set(comb)
            if not is_independent_set(G, comb_as_set):
                continue
            three_coloring = bfs_2_coloring(G, comb_as_set)
            if three_coloring is not None:
                return three_coloring

    G.reset_colors()
    return None


# Feel free to add miscellaneous tests below!
if __name__ == "__main__":
    num_nodes = 40
    prob_edge = 0.075

    total_exhaustive = 0
    total_iset = 0

    num_trials = 5

    for ct in range(num_trials):
        print(f"trial {ct}")
        G = generate_random_graph(Graph, num_nodes, prob_edge)

        start_exhaustive = time()
        exhaustive_search_coloring(G)
        diff = time() - start_exhaustive
        total_exhaustive += diff

        start_iset = time()
        iset_bfs_3_coloring(G)
        diff = time() - start_iset
        total_iset += diff

    print(f"exhaustive: {total_exhaustive / num_trials}")
    print(f"iset: {total_iset / num_trials}")
