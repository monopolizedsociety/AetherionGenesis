# plugins/evaluation_agent_plugin.py

from core.agent_base import Agent
from core.message import Message

class EvaluationAgent(Agent):
    def __init__(self, name, bus):
        super().__init__(name)
        self.bus = bus
        bus.register_agent(name, self)

    def handle(self, message_type, message):
        if message_type == 'meta_result':
            best = message.payload['best']
            print(f"[EvaluationAgent] Best genome:\n{best}")

def register(bus):
    EvaluationAgent('evaluator', bus)
