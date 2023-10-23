from typing import Set, Tuple, Any, Dict

Node = Any
Edge = Tuple[Node, Node]
Graph = Tuple[Set[Node], Set[Edge]]


def independent_set_threshold_decision(graph: Graph, k: int) -> str:
    # ORACLE
    pass


def index_edges(graph: Graph) -> Dict[Node, Node]:
    """Indexes edges by each endpoint"""
    indexed_edges: Dict[Node, Set[Node]] = {}
    [graph_nodes, graph_edges] = graph
    for node in graph_nodes:
        index_edges[node] = set()
    for edge in graph_edges:
        [node1, node2] = edge
        indexed_edges[node1].add(node2)
        indexed_edges[node2].add(node1)
    return indexed_edges


def independent_set_threshold_search(graph: Graph, k: int) -> Set[Node] | None:
    """Finds an independent set of size at least k in G"""
    [graph_nodes, graph_edges] = graph
    indexed_edges: Dict[Node, Set[Node]] = index_edges(graph)
    result_set: Set[Node] = set()

    for node in graph_nodes:
        graph_nodes.remove(node)
        for neighbor in indexed_edges[node]:
            graph_nodes.remove(neighbor)
        # !!! I'm leaving out edges to avoid code bloat.
        # Everywhere a node is removed from the graph, assume all edges
        # related to that node are also removed.
        # Similarly, when a node is re-added, assume its edges are also
        # re-added.
        part_of_res_set = independent_set_threshold_decision(graph, k - 1)
        if part_of_res_set == "YES":
            # keep neighbors out of the remaining graph
            result_set.add(node)
            k -= 1
            continue
        # keep node out, add neighbors back in
        for neighbor in indexed_edges[node]:
            graph_nodes.add(neighbor)

    if len(result_set) < k:
        return None
    return result_set


def independent_set_optimization_search(graph: Graph) -> Set[Node]:
    """Finds the largest independent set in G"""
    lower_bound = 0
    upper_bound = len(graph[0])
    largest: Set[Node] = set()

    while lower_bound <= upper_bound:
        mid = (lower_bound + upper_bound) // 2
        set_geq_mid = independent_set_threshold_search(graph, mid)
        if set_geq_mid is None:
            upper_bound = mid - 1
        else:
            largest = set_geq_mid
            lower_bound = mid + 1

    return largest


def independent_set_threshold_decision(graph: Graph, k: int) -> str:
    largest = independent_set_optimization_search(graph)
    if len(largest) >= k:
        return "YES"
    return "NO"
