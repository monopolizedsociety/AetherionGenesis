# plugins/logging_plugin.py

from core.agent_base import Agent

class LoggingAgent(Agent):
    """
    Logs every message passing through the bus.
    """
    def __init__(self, name, bus):
        super().__init__(name)
        self.bus = bus
        bus.register_agent(name, self)

    def handle(self, message_type, payload):
        print(f"[LoggingAgent] {message_type} -> {payload}")

def register(bus):
    LoggingAgent("logger", bus)
