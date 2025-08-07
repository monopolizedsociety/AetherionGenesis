# plugins/heartbeat_plugin.py

import threading
import time
from core.agent_base import Agent
from core.message import Message

class HeartbeatAgent(Agent):
    """
    Emits a heartbeat message on an interval and updates interval when instructed.
    """
    def __init__(self, name, bus, interval=2):
        super().__init__(name)
        self.bus = bus
        self.interval = interval
        bus.register_agent(name, self)
        bus.register_agent(name + "_adjust", self)  # subscribe to adjust messages
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        while True:
            msg = Message(type="heartbeat", payload={"agent": self.name, "timestamp": time.time()})
            self.bus.dispatch(msg.type, msg)
            time.sleep(self.interval)

    def handle(self, message_type, message):
        if message_type == "heartbeat" and hasattr(message, "payload"):
            # existing heartbeat handling
            print(f"[{self.name}] Received heartbeat: {message.payload}")
        elif message_type == "adjust_interval":
            new_int = message.payload.get("interval")
            print(f"[{self.name}] Adjusting interval from {self.interval} to {new_int}")
            self.interval = new_int

def register(bus):
    HeartbeatAgent("heartbeat", bus, interval=2)
