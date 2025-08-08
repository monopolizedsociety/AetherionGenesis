# core/agent.py

class Agent:
    def __init__(self, name):
        self.name = name

    def handle(self, message):
        raise NotImplementedError("Agent subclasses must implement handle()")
