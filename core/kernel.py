# core/kernel.py
from core.agent_bus import AgentBus
from core.memory_graph import MemoryGraph
from core.plugin_manager import PluginManager

class Kernel:
    """
    Core orchestrator for AetherionPrime:
      - Initializes Bus and MemoryGraph
      - Loads agent plugins
      - Starts the event loop (to be implemented)
    """
    def __init__(self):
        self.bus = AgentBus()
        self.graph = MemoryGraph()
        # expose the graph so agents can query it
        setattr(self.bus, 'graph', self.graph)
        self.plugins = PluginManager(self.bus)

    def bootstrap(self):
        # 1. Initialize graph schema
        self.graph.bootstrap()
        # 2. Load & register built-in agents
        self.bus.register_default_agents()
        # 3. Load external plugins
        self.plugins.load_plugins()
        print("🚀 AetherionPrime Kernel bootstrapped")

if __name__ == "__main__":
    Kernel().bootstrap()
