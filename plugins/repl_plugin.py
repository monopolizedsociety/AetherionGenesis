# plugins/repl_plugin.py
from core.agent_base import Agent
from core.message import new_message

class ReplAgent(Agent):
    def __init__(self, name, bus):
        super().__init__(name)
        self.bus = bus
        bus.register_agent(name, self, subscriptions={})

    def start(self):
        import threading
        def repl_loop():
            while True:
                line = input(">> ")
                m = new_message("command", line.strip())
                self.bus.dispatch("command", m)
        threading.Thread(target=repl_loop, daemon=True).start()

def register(bus):
    agent = ReplAgent("repl", bus)
    agent.start()
