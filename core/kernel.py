# core/kernel.py
import os, threading
from core.agent_bus import AgentBus
from core.memory_graph import MemoryGraph
from core.plugin_manager import PluginManager
from core.consensus import Consensus

class Kernel:
    """
    Core orchestrator for AetherionPrime.
    - MemoryGraph + AgentBus
    - Plugin discovery
    - Optional Raft consensus (CONSENSUS=1)
    """
    def __init__(self):
        self.bus = AgentBus()
        self.graph = MemoryGraph()
        setattr(self.bus, 'graph', self.graph)
        self.plugins = PluginManager(self.bus)

        self.consensus = Consensus() if os.getenv('CONSENSUS','0') == '1' else None

    def bootstrap(self):
        if self.consensus:
            threading.Thread(target=self.consensus.run, daemon=True).start()

        self.graph.bootstrap()
        self.bus.register_default_agents()
        self.plugins.load_plugins()

        if self.consensus:
            print("🚀 AetherionPrime Kernel bootstrapped with Raft consensus")
        else:
            print("🚀 AetherionPrime Kernel bootstrapped")

if __name__ == "__main__":
    Kernel().bootstrap()
