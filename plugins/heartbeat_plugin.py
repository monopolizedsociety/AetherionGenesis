# plugins/heartbeat_plugin.py

import threading
import time
from core.agent_base import Agent
from core.message import Message

class HeartbeatAgent(Agent):
    """
    Emits a heartbeat message on an interval and logs incoming messages.
    """
    def __init__(self, name, bus, interval=2):
        super().__init__(name)
        self.bus = bus
        self.interval = interval
        bus.register_agent(name, self)
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        while True:
            msg = Message(type="heartbeat", payload={
                "agent": self.name,
                "timestamp": time.time()
            })
            self.bus.dispatch(msg.type, msg)
            time.sleep(self.interval)

    def handle(self, message_type, payload):
        print(f"[{self.name}] Received {message_type}: {payload}")

def register(bus):
    HeartbeatAgent("heartbeat", bus, interval=2)
