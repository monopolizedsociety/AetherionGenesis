# plugins/chat_agent_plugin.py

import os
import threading
import openai
from git import Repo
from core.agent_base import Agent
from core.message import Message

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
        if message_type == 'chat':
            user_prompt = message.payload.get('prompt', '')
            # 1. LLM call
            resp = openai.ChatCompletion.create(
                model='gpt-4o-mini',
                messages=[{'role':'user','content':user_prompt}]
            )
            reply = resp.choices[0].message.content
            # 2. Save code if present (assume markdown fenced)
            if '```' in reply:
                code = reply.split('```')[1]
                # simple: save to file named from hash
                filename = f\"generated_{int(time.time())}.py\"
                with open(filename, 'w') as f:
                    f.write(code)
                # 3. Git commit
                self.repo.index.add([filename])
                self.repo.index.commit(f\"feat(chat): add {filename}\")
            # 4. Dispatch response
            self.bus.dispatch('chat_response', Message(type='chat_response', payload={'reply': reply}))
    
    def _dispatch_loop(self):
        # no-op: ChatAgent only reacts to dispatched chat messages
        pass

def register(bus):
    ChatAgent('chat_agent', bus)
