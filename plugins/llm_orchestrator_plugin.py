# plugins/llm_orchestrator_plugin.py
import os
import openai
import time
from core.agent_base import Agent
from core.message import Message

# Set your OpenAI key via: export OPENAI_API_KEY=your_key
openai.api_key = os.getenv('OPENAI_API_KEY')

class LLMOrchestratorAgent(Agent):
    """
    Orchestrates high-level tasks via an LLM:
      - Listens on 'task' messages
      - Retrieves semantic context and graph state
      - Generates a step-by-step plan via OpenAI
      - Dispatches each step as a 'subtask' message
      - Emits a final 'plan_result'
    """
    def __init__(self, name, bus, model='gpt-4o-mini'):
        super().__init__(name)
        self.bus = bus
        self.model = model
        bus.register_agent(name, self)

    def handle(self, message_type, payload):
        if message_type != 'task':
            return

        description = payload.get('description', '')
        # 1. Semantic context (if vmemory exists)
        sem_ctx = []
        if hasattr(self.bus, 'vmemory'):
            emb = openai.Embedding.create(
                model='text-embedding-ada-002',
                input=description
            )['data'][0]['embedding']
            sem_ctx = self.bus.vmemory.search(emb, k=5)

        # 2. Graph snapshot
        nodes = list(self.bus.graph.graph.nodes(data=True))
        edges = list(self.bus.graph.graph.edges(data=True))

        # 3. Build the LLM prompt
        prompt = (
            f"You are an AI OS orchestrator.\n"
            f"Task: {description}\n"
            f"Context Nodes: {nodes}\n"
            f"Context Edges: {edges}\n"
            f"Relevant Memory: {sem_ctx}\n"
            "Generate a numbered list of subtasks to accomplish the task."
        )

        # 4. Call the LLM
        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.2
        )
        plan = resp.choices[0].message.content

        # 5. Dispatch each subtask
        for line in plan.splitlines():
            line = line.strip()
            if line and line[0].isdigit():
                step = line.split('.', 1)[1].strip()
                self.bus.dispatch('subtask', Message(type='subtask', payload={'step': step}))

        # 6. Emit the full plan
        self.bus.dispatch('plan_result', Message(type='plan_result', payload={'plan': plan}))

def register(bus):
    LLMOrchestratorAgent('llm_orchestrator', bus)
