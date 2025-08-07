# aetherion_bootstrap.py

def initialize_genesis_kernel():
    """
    - Load core agent registry
    - Spin up the agent message bus
    - Initialize the dynamic memory graph
    """
    from core.agent_bus import AgentBus
    from core.memory_graph import MemoryGraph

    bus = AgentBus()
    graph = MemoryGraph()

    bus.register_default_agents()
    graph.bootstrap()

    print("✅ Genesis kernel initialized")


if __name__ == "__main__":
    initialize_genesis_kernel()
