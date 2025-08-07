# plugins/webapi_plugin.py

import threading
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from core.agent_base import Agent

class WebAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)
        graph = self.server.bus.graph.graph

        if path == '/nodes':
            resp = list(graph.nodes(data=True))
        elif path == '/edges':
            resp = list(graph.edges(data=True))
        elif path == '/neighbors':
            node = qs.get('node', [None])[0]
            resp = list(graph.successors(node)) if node else {'error': 'node param required'}
        elif path == '/path':
            src = qs.get('src', [None])[0]
            dst = qs.get('dst', [None])[0]
            resp = self.server.bus.graph.find_path(src, dst) if src and dst else {'error': 'src & dst required'}
        else:
            self.send_response(404)
            self.end_headers()
            return

        body = json.dumps(resp).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

class WebAPIAgent(Agent):
    def __init__(self, name, bus, host='0.0.0.0', port=8000):
        super().__init__(name)
        self.bus = bus
        bus.register_agent(name, self)
        self.server = HTTPServer((host, port), WebAPIHandler)
        self.server.bus = bus
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        print(f"[{self.name}] HTTP API running at http://{host}:{port}")

    def handle(self, message_type, payload):
        pass  # does not consume bus messages

def register(bus):
    WebAPIAgent('webapi', bus)
