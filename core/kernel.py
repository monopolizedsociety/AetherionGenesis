# core/kernel.py
# core/kernel.py
import threading
import threading
import os
import os
from core.agent_bus import AgentBus
from core.agent_bus import AgentBus
from core.memory_graph import MemoryGraph
from core.memory_graph import MemoryGraph
from core.plugin_manager import PluginManager
from core.plugin_manager import PluginManager
from core.consensus import Consensus
from core.consensus import Consensus


class Kernel:
class Kernel:
    """
    """
    Core orchestrator for AetherionPrime with Raft-based consensus.
    Core orchestrator for AetherionPrime with Raft-based consensus.
    """
    """
    def __init__(self):
    def __init__(self):
        import os
        self.bus = AgentBus()
        self.bus = AgentBus()
        self.graph = MemoryGraph()
        self.graph = MemoryGraph()
        setattr(self.bus, 'graph', self.graph)
        setattr(self.bus, 'graph', self.graph)
        self.plugins = PluginManager(self.bus)
        self.plugins = PluginManager(self.bus)


        # Initialize consensus
        # Initialize consensus
        self.consensus = Consensus() if os.getenv('CONSENSUS','0') == '1' else None
        self.consensus = Consensus() if os.getenv('CONSENSUS','0') == '1' else None


    def bootstrap(self):
    def bootstrap(self):
        # Start the Raft node in a daemon thread
        # Start the Raft node in a daemon thread
        if self.consensus:
            threading.Thread(target=self.consensus.run, daemon=True).start()
        if self.consensus:
            threading.Thread(target=self.consensus.run, daemon=True).start()


        # 1. Initialize graph schema
        # 1. Initialize graph schema
        self.graph.bootstrap()
        self.graph.bootstrap()
        # 2. Register built-in agents
        # 2. Register built-in agents
        self.bus.register_default_agents()
        self.bus.register_default_agents()
        # 3. Load external plugins
        # 3. Load external plugins
        self.plugins.load_plugins()
        self.plugins.load_plugins()


        print("🚀 AetherionPrime Kernel bootstrapped with Raft consensus")
        print("🚀 AetherionPrime Kernel bootstrapped with Raft consensus")


if __name__ == "__main__":
if __name__ == "__main__":
    Kernel().bootstrap()
    Kernel().bootstrap()
