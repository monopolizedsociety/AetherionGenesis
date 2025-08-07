# core/agent_bus.py

class AgentBus:
    """
    Simple message bus for registering and dispatching messages between agents.
    """
    def __init__(self):
        self._agents = {}

    def register_agent(self, name: str, agent):
        """Register an agent under a unique name."""
        self._agents[name] = agent

    def register_default_agents(self):
        """Register all built-in agents (to be implemented)."""
        # TODO: import and register core agents
        pass

    def dispatch(self, message_type: str, payload):
        """
        Send a message of a given type to all interested agents.
        """
        for agent in self._agents.values():
            agent.handle(message_type, payload)
