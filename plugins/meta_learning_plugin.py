# plugins/meta_learning_plugin.py

import os
import time
import random
import openai
import importlib
from deap import base, creator, tools
from core.agent_base import Agent
from core.message import Message

# Make sure OPENAI_API_KEY is set in your environment
openai.api_key = os.getenv('OPENAI_API_KEY')

class MetaLearningAgent(Agent):
    """
    Auto-generates, tests, and installs new agent plugins
    via LLM + genetic search.
    """
    def __init__(self, name, bus, population=5, generations=3):
        super().__init__(name)
        self.bus = bus
        self.population = population
        self.generations = generations
        bus.register_agent(name, self)

    def handle(self, message_type, message):
        if message_type != 'meta_train':
            return

        # 1. Set up Genetic Algorithm
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
        toolbox = base.Toolbox()
        toolbox.register("attr_prompt", self.random_prompt)
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_prompt, n=3)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("evaluate", self.evaluate_candidate)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
        toolbox.register("select", tools.selBest)

        pop = toolbox.population(n=self.population)
        for _ in range(self.generations):
            fitnesses = list(map(toolbox.evaluate, pop))
            for ind, fit in zip(pop, fitnesses):
                ind.fitness.values = (fit,)
            pop = toolbox.select(pop, k=self.population)
            offspring = tools.selRoulette(pop, k=self.population)
            offspring = list(map(toolbox.clone, offspring))
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < 0.5:
                    toolbox.mate(child1, child2)
                toolbox.mutate(child1)
            pop[:] = offspring

        best = tools.selBest(pop, k=1)[0]
        self.bus.dispatch('meta_result', Message(type='meta_result', payload={'best': best}))

    def random_prompt(self):
        return "Write a Python Agent plugin for Aetherion that logs every message with timestamp."

    def evaluate_candidate(self, individual):
        prompt = "\\n".join(individual)
        resp = openai.ChatCompletion.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': prompt}]
        )
        code = resp.choices[0].message.content
        fname = f"plugins/gen_{int(time.time())}.py"
        with open(fname, 'w') as f:
            f.write(code)
        try:
            importlib.import_module(f"plugins.{os.path.basename(fname)[:-3]}")
            start = time.time()
            self.bus.dispatch('heartbeat', Message(type='heartbeat', payload={}))
            duration = time.time() - start
            return max(0.0, 1.0 - duration)
        except Exception:
            return 0.0

def register(bus):
    MetaLearningAgent('meta_learning', bus)
