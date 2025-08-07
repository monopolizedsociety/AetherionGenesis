# plugins/scheduler_plugin.py

import threading
import time
from core.agent_base import Agent
from core.message import Message

class SchedulerAgent(Agent):
    """
    Emits a 'tick' message on the bus at specified intervals.
    """
    def __init__(self, name, bus, interval=5):
        super().__init__(name)
        self.bus = bus
        bus.register_agent(name, self)
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        count = 0
        while True:
            msg = Message(type="tick", payload={"count": count, "timestamp": time.time()})
            self.bus.dispatch(msg.type, msg)
            count += 1
            time.sleep(self.interval)

    def handle(self, message_type, payload):
        # log each tick
        print(f"[{self.name}] Tick #{payload['count']} at {payload['timestamp']}")

def register(bus):
    SchedulerAgent("scheduler", bus, interval=5)
