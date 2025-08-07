# plugins/query_plugin.py

from core.agent_base import Agent
from core.message import Message

class QueryAgent(Agent):
    """
    Listens for 'command' messages to query the MemoryGraph.
    Commands:
      - nodes            : list all nodes
      - edges            : list all edges
      - neighbors <id>   : list successors of a node
      - path <src> <dst> : find shortest path
    """
    def __init__(self, name, bus):
        super().__init__(name)
        self.bus = bus
        bus.register_agent(name, self)

    def handle(self, message_type, payload):
        if message_type == "command":
            parts = payload.split()
            cmd, args = parts[0], parts[1:]
            if cmd == "nodes":
                print("[QueryAgent] Nodes:", list(self.bus.graph.graph.nodes))
            elif cmd == "edges":
                print("[QueryAgent] Edges:", list(self.bus.graph.graph.edges(data=True)))
            elif cmd == "neighbors" and len(args) == 1:
                n = self.bus.graph.get_neighbors(args[0])
                print(f"[QueryAgent] Neighbors of {args[0]}:", n)
            elif cmd == "path" and len(args) == 2:
                p = self.bus.graph.find_path(args[0], args[1])
                print(f"[QueryAgent] Path {args[0]}→{args[1]}:", p)
            else:
                print("[QueryAgent] Unknown command:", payload)
