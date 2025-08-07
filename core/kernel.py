import threading
import time
import os

from core.agent_bus import AgentBus
from core.plugin_manager import PluginManager
from core.message import Message
from core.consensus import ConsensusNode
from core.repl import start_repl

class Kernel:
    def __init__(self):
        self.bus = AgentBus()
        self.plugins = PluginManager(self.bus)

    def bootstrap(self):
        print("🚀 Bootstrapping AetherionPrime Kernel...")

        # Start core agents
        from agents.echo_agent import EchoAgent
        from agents.logging_agent import LoggingAgent
        from agents.heartbeat_agent import HeartbeatAgent
        from agents.scheduler_agent import SchedulerAgent
        from agents.perception_agent import PerceptionAgent

        self.bus.register(EchoAgent())
        self.bus.register(LoggingAgent())
        self.bus.register(HeartbeatAgent())
        self.bus.register(SchedulerAgent(interval=5))
        self.bus.register(PerceptionAgent())

        # Start plugin loader
        plugin_thread = threading.Thread(target=self.plugins.load_plugins, daemon=True)
        plugin_thread.start()

        # Start consensus if env configured
        if os.environ.get("RAFT_ID"):
            node_id = os.environ["RAFT_ID"]
            peers = os.environ.get("RAFT_PEERS", "")
            peers = peers.split(",") if peers else []
            consensus = ConsensusNode(self.bus, node_id, peers)
            consensus_thread = threading.Thread(target=consensus.run, daemon=True)
            consensus_thread.start()
        else:
            print("[consensus] Not configured. Set RAFT_ID to enable.")

        # Start REPL (interactive shell)
        start_repl(self.bus)

if __name__ == "__main__":
    Kernel().bootstrap()
