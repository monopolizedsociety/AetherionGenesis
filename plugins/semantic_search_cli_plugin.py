# plugins/semantic_search_cli_plugin.py

import os
import openai
from core.agent_base import Agent

openai.api_key = os.getenv('OPENAI_API_KEY')

class SemanticSearchCLI(Agent):
    """
    Extends the CLI: when a 'command' starts with 'search ',
    embed the query and search VectorMemory for nearest items.
    """
    def __init__(self, name, bus, k=5):
        super().__init__(name)
        self.bus = bus
        self.k = k
        # receive only CLI 'command' messages
        bus.register_agent(name, self, subscriptions={'command'})

    def handle(self, message_type, message):
        if message_type != 'command':
            return
        cmd = message.payload.strip()
        if not cmd.lower().startswith("search "):
            return
        query = cmd[len("search "):].strip()
        if not hasattr(self.bus, 'vmemory'):
            print("[SemanticSearch] No vector memory available.")
            return
        if not openai.api_key:
            print("[SemanticSearch] OPENAI_API_KEY not set; cannot embed query.")
            return
        try:
            emb = openai.Embedding.create(
                model="text-embedding-ada-002",
                input=query
            )['data'][0]['embedding']
            results = self.bus.vmemory.search(emb, k=self.k)
            print("[SemanticSearch] Top results:")
            for meta, dist in results:
                print(f"  - dist={dist:.4f} :: {meta}")
        except Exception as e:
            print("[SemanticSearch] Error:", e)

def register(bus):
    SemanticSearchCLI("semantic_cli", bus)
