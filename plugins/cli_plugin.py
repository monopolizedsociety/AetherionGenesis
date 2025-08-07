# plugins/cli_plugin.py

import threading
from core.agent_base import Agent
from core.message import Message

class CLIAgent(Agent):
    """
    Reads lines from stdin and dispatches them as 'command' messages.
    """
    def __init__(self, name, bus):
        super().__init__(name)
        self.bus = bus
        bus.register_agent(name, self)
        threading.Thread(target=self._read_loop, daemon=True).start()

    def _read_loop(self):
        while True:
            try:
                cmd = input()
                if cmd.strip():
                    msg = Message(type="command", payload=cmd.strip())
                    self.bus.dispatch(msg.type, msg)
            except EOFError:
                break

    def handle(self, message_type, payload):
        if message_type == "command":
            print(f"[CLIAgent] Executing command: {payload}")

def register(bus):
    CLIAgent("cli", bus)
