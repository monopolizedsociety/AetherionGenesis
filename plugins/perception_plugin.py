# plugins/perception_plugin.py

import os
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image
from core.agent_base import Agent
from core.message import Message

def detect_objects_stub(image_path):
    """
    Stub for object detection. Replace with a real model call.
    """
    # For now, return a dummy list
    return ["object1", "object2"]

class PerceptionHandler(FileSystemEventHandler):
    def __init__(self, bus):
        super().__init__()
        self.bus = bus

    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            objects = detect_objects_stub(event.src_path)
            node_id = os.path.basename(event.src_path)
            # Add image node
            self.bus.graph.add_node(node_id, {"type": "percept", "file": event.src_path})
            # Add object nodes + edges
            for obj in objects:
                self.bus.graph.add_node(obj, {"type": "object"})
                self.bus.graph.add_edge(node_id, obj, "contains")
            # Emit a perception message
            msg = Message(type="perception", payload={"file": event.src_path, "objects": objects})
            self.bus.dispatch(msg.type, msg)

class PerceptionAgent(Agent):
    def __init__(self, name, bus, watch_dir="percepts"):
        super().__init__(name)
        self.bus = bus
        self.watch_dir = watch_dir
        os.makedirs(watch_dir, exist_ok=True)
        bus.register_agent(name, self)
        handler = PerceptionHandler(bus)
        observer = Observer()
        observer.schedule(handler, path=watch_dir, recursive=False)
        observer.daemon = True
        observer.start()
        print(f"[{name}] Watching directory: {watch_dir}")

    def handle(self, message_type, payload):
        print(f"[PerceptionAgent] Processed: {payload}")

def register(bus):
    PerceptionAgent('perception', bus)
