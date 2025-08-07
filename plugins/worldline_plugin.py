# plugins/worldline_plugin.py
import copy
import networkx as nx
from core.agent_base import Agent
from core.message import new_message

class WorldlineAgent(Agent):
    """
    Counterfactual simulator: applies hypothetical actions to a cloned graph and returns a diff.
    Supported actions:
      - {"type": "graph.add_node", "payload": {"id": "<node_id>", "data": {...}}}
      - {"type": "graph.add_edge", "payload": {"src": "A", "dst": "B", "relation": "label"}}
    """
    def __init__(self, name, bus):
        super().__init__(name)
        self.bus = bus
        bus.register_agent(name, self, subscriptions={'simulate'})

    def handle(self, message_type, message):
        if message_type != 'simulate':
            return
        orig = self.bus.graph.graph
        cloned = nx.DiGraph(orig)   # shallow copy of structure & attributes

        for action in message.payload.get("actions", []):
            typ = action.get("type")
            pay = action.get("payload", {})
            try:
                if typ == "graph.add_node":
                    cloned.add_node(pay["id"], **(pay.get("data", {})))
                elif typ == "graph.add_edge":
                    cloned.add_edge(pay["src"], pay["dst"], relation=pay.get("relation","rel"))
            except Exception as e:
                print("[worldline] action error:", e)

        # compute diffs
        added_nodes = list(set(cloned.nodes()) - set(orig.nodes()))
        added_edges = list(set(cloned.edges()) - set(orig.edges()))
        result = {"added_nodes": added_nodes, "added_edges": [(u,v) for (u,v) in added_edges]}
        self.bus.dispatch("simulation_result", new_message("simulation_result", result, parent_cid=message.cid))

def register(bus):
    WorldlineAgent("worldline", bus)
