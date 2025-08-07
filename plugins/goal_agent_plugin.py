# plugins/goal_agent_plugin.py

import os
import openai
from core.agent_base import Agent
from core.message import Message

openai.api_key = os.getenv('OPENAI_API_KEY')

class GoalAgent(Agent):
    """
    Converts high-level 'goal' messages into concrete 'task' messages.
    - If OPENAI_API_KEY is set, uses LLM to decompose the goal.
    - Otherwise, uses a simple heuristic fallback.
    """
    def __init__(self, name, bus):
        super().__init__(name)
        self.bus = bus
        # subscribe only to 'goal'
        bus.register_agent(name, self, subscriptions={'goal'})

    def handle(self, message_type, message):
        if message_type != 'goal':
            return
        description = message.payload.get('description', '').strip()
        steps = self._decompose(description)
        for step in steps:
            self.bus.dispatch('task', Message(type='task', payload={'description': step}))
        # also emit a goal_result summary
        self.bus.dispatch('goal_result', Message(type='goal_result', payload={'goal': description, 'steps': steps}))

    def _decompose(self, text: str):
        if openai.api_key:
            try:
                resp = openai.ChatCompletion.create(
                    model='gpt-4o-mini',
                    messages=[{'role':'user','content': f"Decompose this goal into 5 concrete steps:\n{text}"}],
                    temperature=0.2
                )
                content = resp.choices[0].message.content
                steps = [line.split('.',1)[1].strip() for line in content.splitlines() if line.strip() and line[0].isdigit() and '.' in line]
                return steps or [text]
            except Exception as e:
                print("[GoalAgent] LLM error:", e)
        # Fallback: naive heuristics
        if "path" in text and "->" in text:
            parts = [p.strip() for p in text.split("->")]
            if len(parts) == 2:
                a,b = parts
                return [f"Plan route from {a} to {b}", f"Summarize route from {a} to {b}"]
        return [text]

def register(bus):
    GoalAgent("goals", bus)
