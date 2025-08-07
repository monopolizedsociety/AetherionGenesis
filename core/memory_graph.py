# core/memory_graph.py
import networkx as nx

class MemoryGraph:
    """
    Dynamic memory graph to track entities and relationships over time,
    built on networkx for powerful graph algorithms.
    """
    def __init__(self):
        self.graph = nx.DiGraph()

    def bootstrap(self):
        """Initialize graph schema and any default nodes."""
        # add a root kernel node
        self.graph.add_node("root", type="kernel")

    def add_node(self, node_id: str, data: dict):
        """Add or update a node in the graph."""
        self.graph.add_node(node_id, **data)

    def add_edge(self, from_id: str, to_id: str, relation: str):
        """Create a directed, labeled edge between two nodes."""
        self.graph.add_edge(from_id, to_id, relation=relation)

    def get_neighbors(self, node_id: str):
        """Return successors of a given node."""
        return list(self.graph.successors(node_id))

    def find_path(self, source: str, target: str):
        """Return shortest path or None if no path exists."""
        try:
            return nx.shortest_path(self.graph, source, target)
        except nx.NetworkXNoPath:
            return None
