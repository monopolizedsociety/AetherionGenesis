# plugins/vector_memory_plugin.py
import time
import openai
from core.agent_base import Agent
from core.message import Message
from core.vector_memory import VectorMemory

class VectorMemoryAgent(Agent):
    \"\"\"
    Computes embeddings for each message and stores them in a FAISS index.
    Requires OPENAI_API_KEY in env.
    \"\"\"
    def __init__(self, name, bus, model="text-embedding-ada-002", dim=1536):
        super().__init__(name)
        self.bus = bus
        self.model = model
        self.vmemory = VectorMemory(dim)
        setattr(bus, 'vmemory', self.vmemory)
        bus.register_agent(name, self)

    def handle(self, message_type, payload):
        text = f\"{message_type}:{payload}\"
        resp = openai.Embedding.create(model=self.model, input=text)
        vector = resp['data'][0]['embedding']
        self.vmemory.add(vector, {
            "type": message_type,
            "payload": payload,
            "timestamp": time.time()
        })

def register(bus):
    VectorMemoryAgent("vector_memory", bus)
