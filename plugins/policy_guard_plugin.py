# plugins/policy_guard_plugin.py
import json, os
from core.agent_base import Agent
from core.message import Message, new_message
from core import caps as caps

SAFE_DIR = "var/sandbox"

class PolicyGuard(Agent):
    def __init__(self, name, bus):
        super().__init__(name)
        self.bus = bus
        bus.register_agent(name, self, subscriptions={'cap_request'})

    def handle(self, message_type, message):
        if message_type == "cap_request":
            scopes = message.payload.get("scopes", [])
            ttl = int(message.payload.get("ttl", 300))
            token = caps.mint(scopes, ttl_seconds=ttl)
            print(f"[cap] issued token for {scopes}, ttl={ttl}s")
            self.bus.dispatch("cap_issued", new_message("cap_issued", {"token": token}, parent_cid=message.cid))

class SyscallAgent(Agent):
    def __init__(self, name, bus):
        super().__init__(name)
        self.bus = bus
        os.makedirs(SAFE_DIR, exist_ok=True)
        bus.register_agent(name, self, subscriptions={'fs_write'})

    def handle(self, message_type, message):
        if message_type != "fs_write":
            return
        token = (message.metadata or {}).get("cap") or message.payload.get("cap")
        ok, info = caps.verify(token, "fs.write")
        if not ok:
            print(f"[syscall] denied: {info}")
            return
        rel = message.payload.get("path", "out.txt").replace("..", "_")
        path = os.path.join(SAFE_DIR, rel)
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(message.payload.get("content", "")))
        print(f"[syscall] wrote {path}")

def register(bus):
    PolicyGuard("policy", bus)
    SyscallAgent("sys", bus)
