from core.agent import Agent
from core.message import Message
import time

class EchoAgent(Agent):
    def handle_message(self, message: Message):
        if message.type == "heartbeat":
            self.send("heartbeat", Message("heartbeat", {"agent": "heartbeat", "timestamp": time.time()}))
        elif message.type == "tick":
            self.send("echo", message)
