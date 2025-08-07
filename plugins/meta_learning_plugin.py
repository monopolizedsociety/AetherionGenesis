# plugins/meta_learning_plugin.py

import os
import time
import openai
import importlib
import shutil
from deap import base, creator, tools
from core.agent_base import Agent
from core.message import Message

openai.api_key = os.getenv('OPENAI_API_KEY')

class MetaLearningAgent(Agent):
    \"\"\"
    Auto-generates, tests, and installs new agent plugins via LLM + genetic search.
    \"\"\"
    def __init__(self, name, bus, population=5, generations=3):
        super().__init__(name)
        self.bus = bus
        self.population = population
        self.generations = generations
        bus.register_agent(name, self)

    def handle(self, message_type, message):
        if message_type == 'meta_train':
            # 1. Initialize GA toolbox
            creator.create("FitnessMax", base.Fitness, weights=(1.0,))
            creator.create("Individual", list, fitness=creator.FitnessMax)
            toolbox = base.Toolbox()
            # Define genome as list of prompts
            toolbox.register("attr_prompt", self.random_prompt)
            toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_prompt, n=3)
            toolbox.register("population", tools.initRepeat, list, toolbox.individual)
            toolbox.register("evaluate", self.evaluate_candidate)
            toolbox.register("mate", tools.cxTwoPoint)
            toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
            toolbox.register("select", tools.selBest)

            pop = toolbox.population(n=self.population)
            for gen in range(self.generations):
                # Evaluate all
                fitnesses = list(map(toolbox.evaluate, pop))
                for ind, fit in zip(pop, fitnesses):
                    ind.fitness.values = (fit,)
                # Select, mate, mutate
                pop = toolbox.select(pop, k=self.population)
                offspring = tools.selRoulette(pop, k=self.population)
                offspring = list(map(toolbox.clone, offspring))
                for child1, child2 in zip(offspring[::2], offspring[1::2]):
                    if random.random() < 0.5:
                        toolbox.mate(child1, child2)
                    toolbox.mutate(child1)
                pop[:] = offspring
            # Best individual
            best = tools.selBest(pop, k=1)[0]
            msg = Message(type='meta_result', payload={'best': best})
            self.bus.dispatch('meta_result', msg)

    def random_prompt(self):
        # Create a random prompt to LLM for generating new agent code
        return "Write a Python Agent plugin for Aetherion that logs every message with timestamp."

    def evaluate_candidate(self, individual):
        # Synthesize candidate code via LLM
        prompt = "\\n".join(individual)
        resp = openai.ChatCompletion.create(
            model='gpt-4o-mini',
            messages=[{'role':'user','content':prompt}]
        )
        code = resp.choices[0].message.content
        # Save and load as plugin to test
        fname = f"plugins/gen_{int(time.time())}.py"
        with open(fname, 'w') as f:
            f.write(code)
        try:
            mod = importlib.import_module(f"plugins.{os.path.basename(fname)[:-3]}")
            # Simple test: dispatch a test message and measure no errors
            start = time.time()
            self.bus.dispatch('heartbeat', Message(type='heartbeat', payload={}))
            duration = time.time() - start
            return max(0, 1.0 - duration)  # faster is better
        except Exception:
            return 0.0
