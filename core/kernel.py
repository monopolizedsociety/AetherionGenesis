# core/kernel.py
import threading
import os
from core.agent_bus import AgentBus
from core.memory_graph import MemoryGraph
from core.plugin_manager import PluginManager
from core.consensus import Consensus

class Kernel:
    """
    Core orchestrator for AetherionPrime with Raft-based consensus.
    """
    def __init__(self):
        self.bus = AgentBus()
        self.graph = MemoryGraph()
        setattr(self.bus, 'graph', self.graph)
        self.plugins = PluginManager(self.bus)

        # Initialize consensus
        self.consensus = Consensus()

    def bootstrap(self):
        # Start the Raft node in a daemon thread
        threading.Thread(target=self.consensus.run, daemon=True).start()

        # 1. Initialize graph schema
        self.graph.bootstrap()
        # 2. Register built-in agents
        self.bus.register_default_agents()
        # 3. Load external plugins
        self.plugins.load_plugins()

        print("🚀 AetherionPrime Kernel bootstrapped with Raft consensus")

if __name__ == "__main__":
    Kernel().bootstrap()
