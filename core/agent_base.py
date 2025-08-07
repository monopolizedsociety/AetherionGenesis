# core/agent_base.py

class Agent:
    """
    Base class for all agents in the Aetherion civilization.
    """
    def __init__(self, name: str):
        self.name = name

    def handle(self, message_type: str, payload):
        """
        Called by the AgentBus when a message of message_type arrives.
        Must be overridden by subclasses.
        """
        raise NotImplementedError("Agents must implement handle()")
