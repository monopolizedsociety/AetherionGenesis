# plugins/chat_agent_plugin.py

import os
import threading
import time
import openai
from git import Repo
from core.agent_base import Agent
from core.message import Message

# Ensure your OPENAI_API_KEY is set in the environment
openai.api_key = os.getenv('OPENAI_API_KEY')

class ChatAgent(Agent):
    """
    Conversational agent: takes 'chat' messages, asks the LLM, writes code, and commits.
    """
    def __init__(self, name, bus, repo_path='.'):
        super().__init__(name)
        self.bus = bus
        self.repo = Repo(repo_path)
        bus.register_agent(name, self)
        threading.Thread(target=self._dispatch_loop, daemon=True).start()

    def handle(self, message_type, message):
        if message_type != 'chat':
            return

        user_prompt = message.payload.get('prompt', '')
        # 1. Call the LLM
        resp = openai.ChatCompletion.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': user_prompt}]
        )
        reply = resp.choices[0].message.content

        # 2. Extract and save code if fenced in markdown
        if '```' in reply:
            code = reply.split('```')[1]
            filename = f"generated_{int(time.time())}.py"
            with open(filename, 'w') as f:
                f.write(code)
            # 3. Commit the new file
            self.repo.index.add([filename])
            self.repo.index.commit(f"feat(chat): add {filename}")

        # 4. Dispatch the LLM reply back on the bus
        self.bus.dispatch(
            'chat_response',
            Message(type='chat_response', payload={'reply': reply})
        )

    def _dispatch_loop(self):
        # ChatAgent only responds to 'chat' messages—no polling needed
        pass

def register(bus):
    ChatAgent('chat_agent', bus)
