# plugins/echo_plugin.py

from core.agent_base import Agent
from core.message import Message

class EchoAgent(Agent):
    """
    Echoes any non-echo message back on the 'echo' channel.
    """
    def __init__(self, name, bus):
        super().__init__(name)
        self.bus = bus
        bus.register_agent(name, self)

    def handle(self, message_type, payload):
        if message_type != "echo":
            print(f"[EchoAgent] Echoing {message_type}")
            msg = Message(type="echo", payload=payload)
            self.bus.dispatch(msg.type, msg)

def register(bus):
    EchoAgent("echoer", bus)
