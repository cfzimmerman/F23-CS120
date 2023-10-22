from typing import Set, Tuple, Any

Node = Any
Edge = Tuple[Node, Node]
Graph = Tuple[Set[Node], Set[Edge]]


def independent_set_optimization_search(graph: Graph) -> Set[Node]:
    # ORACLE
    pass


def independent_set_threshold_decision(graph: Graph, k: int) -> str:
    largest = independent_set_optimization_search(graph)
    if len(largest) >= k:
        return "YES"
    return "NO"
