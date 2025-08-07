# plugins/rl_agent_plugin.py

import threading
import time
import random
from core.agent_base import Agent
from core.message import Message

class RLAgent(Agent):
    """
    Reinforcement Learning agent that adjusts the HeartbeatAgent's interval
    based on tick-rate rewards.
    """
    def __init__(self, name, bus, target_rate=1.0):
        super().__init__(name)
        self.bus = bus
        self.target_rate = target_rate  # desired ticks per second
        self.heartbeat_agent = None
        self.intervals = [0.5, 1.0, 2.0, 5.0]
        self.q_values = {i: 0.0 for i in self.intervals}
        bus.register_agent(name, self)
        # Listen for subtask to grab heartbeat agent
        bus.register_agent(name, self)
        # Start periodic evaluation
        threading.Thread(target=self.evaluate_loop, daemon=True).start()

    def handle(self, message_type, message):
        # Capture reference to HeartbeatAgent instance
        if message_type == "heartbeat":
            if not self.heartbeat_agent:
                # when heartbeat first fires, find the agent by name
                self.heartbeat_agent = self.bus._agents.get("heartbeat")
    
    def evaluate_loop(self):
        while not self.heartbeat_agent:
            time.sleep(0.1)
        while True:
            # Compute reward: difference between actual rate and target
            # (stub: random reward)
            action = random.choice(self.intervals)
            reward = random.uniform(-1, 1)
            # Update Q-value (simplified)
            self.q_values[action] += 0.1 * (reward - self.q_values[action])
            # Pick the best interval
            best = max(self.q_values, key=lambda k: self.q_values[k])
            # Dispatch an adjust_interval message
            self.bus.dispatch("adjust_interval", Message(type="adjust_interval", payload={"interval": best}))
            time.sleep(10)

def register(bus):
    RLAgent("rl_agent", bus)
