# plugins/audit_plugin.py
from core.agent_base import Agent
from core.audit_store import append

class AuditAgent(Agent):
    def __init__(self, name, bus):
        super().__init__(name)
        self.bus = bus
        bus.register_agent(name, self, subscriptions={'*'})

    def handle(self, message_type, message):
        # Only log Message instances (not plain payloads)
        try:
            if hasattr(message, "type") and hasattr(message, "cid"):
                append(message)
        except Exception as e:
            print("[audit] error:", e)

def register(bus):
    AuditAgent("audit", bus)
