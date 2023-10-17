from typing import Tuple, List, Set

NodeID = int
InputEdge = Tuple[NodeID, NodeID]
InputGraph = Tuple[Set[NodeID], List[InputEdge]]

OriginGraphID = int
ModifiedNodeID = Tuple[NodeID, OriginGraphID]
ModifiedEdge = Tuple[ModifiedNodeID, ModifiedNodeID]
ModifiedGraph = Tuple[Set[ModifiedNodeID], List[ModifiedEdge]]


def single_source_shortest_walk(
    graph: ModifiedGraph,
    start: ModifiedNodeID,
    end: NodeID,
) -> List[ModifiedEdge]:
    # ORACLE CALL
    """This assumes an oracle conceptually similar to single source
    shortest path from class except only the shortest path is returned,
    not the length of every path from v to s.
    It also assumes the oracle can properly operate on (NodeID, GraphID)
    keys to return any such key where NodeID reaches `end`, regardless of
    the ending GraphID. That simplifies the (already long) code."""
    pass


def shortest_rotating_walk(
    input_graphs: List[InputGraph], s: NodeID, t: NodeID
) -> List[ModifiedEdge]:
    modified_graph_nodes: Set[ModifiedNodeID] = set()
    modified_graph_edges: List[ModifiedEdge] = []

    # PREPROCESSING: Create the modified graph
    for graph_num, (graph_nodes, graph_edges) in enumerate(input_graphs):
        # curr_graph_num counts from 0 to k - 1 for k - 1 input graphs
        next_graph_num: int = (graph_num + 1) % (len(input_graphs) - 1)

        for node in graph_nodes:
            # add every node to the modified graph
            modified_node_id: ModifiedNodeID = (node, graph_num)
            modified_graph_nodes.add(modified_node_id)

        for origin, destination in graph_edges:
            # add every edge to the modified graph
            origin_node: ModifiedNodeID = (origin, graph_num)
            destination_node: ModifiedNodeID = (destination, next_graph_num)
            modified_edge: ModifiedEdge = (origin_node, destination_node)
            # notice the origin and destination now pass from one input GraphID
            # to the next
            modified_graph_edges.append(modified_edge)

    modified_graph: ModifiedGraph = (modified_graph_nodes, modified_graph_edges)
    start_node_id: ModifiedNodeID = (s, 0)
    end_node_id: NodeID = t

    # ORACLE CALL
    path = single_source_shortest_walk(modified_graph, start_node_id, end_node_id)

    return path
