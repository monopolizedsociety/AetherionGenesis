# core/memory_graph.py

class MemoryGraph:
    """
    Dynamic memory graph to track entities and relationships over time.
    """
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def bootstrap(self):
        """Initialize graph schema and any default nodes."""
        # TODO: set up initial graph state
        pass

    def add_node(self, node_id: str, data: dict):
        """Add or update a node in the graph."""
        self.nodes[node_id] = data

    def add_edge(self, from_id: str, to_id: str, relation: str):
        """Create a directed edge between two nodes."""
        self.edges.append((from_id, to_id, relation))
