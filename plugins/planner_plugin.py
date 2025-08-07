# plugins/planner_plugin.py

from core.agent_base import Agent
from core.message import Message
import heapq

class PlannerAgent(Agent):
    """
    Listens for 'plan' messages with payload {'start','goal'}
    and replies with a shortest path via A* on the graph.
    """
    def __init__(self, name, bus):
        super().__init__(name)
        self.bus = bus
        bus.register_agent(name, self)

    def handle(self, message_type, payload):
        if message_type == "plan":
            start, goal = payload["start"], payload["goal"]
            path = self._astar(start, goal)
            msg = Message(type="plan_result", payload={"path": path})
            self.bus.dispatch(msg.type, msg)

    def _astar(self, start, goal):
        graph = self.bus.graph.graph
        # simple A* with heuristic=0 (Dijkstra)
        queue = [(0, start, [start])]
        seen = set()
        while queue:
            cost, node, path = heapq.heappop(queue)
            if node == goal:
                return path
            if node in seen:
                continue
            seen.add(node)
            for nbr in graph.successors(node):
                if nbr not in seen:
                    heapq.heappush(queue, (cost+1, nbr, path+[nbr]))
        return None

def register(bus):
    PlannerAgent("planner", bus)
