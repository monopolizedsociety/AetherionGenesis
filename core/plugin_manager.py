# core/plugin_manager.py
import importlib
import os

class PluginManager:
    """
    Dynamically discover and load agent plugins from the 'plugins' directory.
    """
    def __init__(self, bus):
        self.bus = bus

    def load_plugins(self):
        for fname in os.listdir('plugins'):
            if fname.endswith('.py') and fname != '__init__.py':
                mod_name = f"plugins.{fname[:-3]}"
                module = importlib.import_module(mod_name)
                if hasattr(module, 'register'):
                    module.register(self.bus)
