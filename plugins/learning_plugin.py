# plugins/learning_plugin.py

from core.agent_base import Agent
from core.message import Message

class LearningAgent(Agent):
    """
    Aggregates counts of each message type seen and dumps stats on 'stats' command.
    """
    def __init__(self, name, bus):
        super().__init__(name)
        self.bus = bus
        self.counts = {}
        bus.register_agent(name, self)

    def handle(self, message_type, payload):
        # increment count
        self.counts[message_type] = self.counts.get(message_type, 0) + 1
        if message_type == "command" and payload.strip() == "stats":
            msg = Message(type="stats_result", payload=self.counts.copy())
            self.bus.dispatch(msg.type, msg)

def register(bus):
    LearningAgent("learner", bus)
