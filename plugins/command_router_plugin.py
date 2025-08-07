# plugins/command_router_plugin.py
import json
from core.agent_base import Agent
from core.message import Message, new_message

class CommandRouterAgent(Agent):
    def __init__(self, name, bus):
        super().__init__(name)
        self.bus = bus
        bus.register_agent(name, self, subscriptions={'command'})

    def handle(self, message_type, message):
        if message_type != "command":
            return
        line = message.payload.strip()
        try:
            if line.startswith("cap "):
                # cap <scope> <minutes>
                _, scope, mins = line.split(maxsplit=2)
                ttl = int(float(mins) * 60)
                self.bus.dispatch("cap_request", new_message("cap_request", {"scopes":[scope], "ttl": ttl}, parent_cid=message.cid))
            elif line.startswith("fs_write "):
                # fs_write {"path":"x","content":"y","cap":"..."}
                data = json.loads(line[len("fs_write "):])
                m = new_message("fs_write", data, metadata={"cap": data.get("cap")}, parent_cid=message.cid)
                self.bus.dispatch("fs_write", m)
            elif line.startswith("simulate "):
                # simulate {"actions":[{"type":"graph.add_node","payload":{"id":"n1","data":{"k":"v"}}}]}
                data = json.loads(line[len("simulate "):])
                self.bus.dispatch("simulate", new_message("simulate", data, parent_cid=message.cid))
        except Exception as e:
            print("[router] parse error:", e)

def register(bus):
    CommandRouterAgent("router", bus)
