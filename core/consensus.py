import os, asyncio, raftos

def _valid(addr: str) -> bool:
    return isinstance(addr, str) and ':' in addr and addr.strip()

class Consensus:
    def __init__(self, node_id=None, peers=None):
        self.node_id = node_id or os.getenv('RAFT_ID', '')
        peers_env = os.getenv('RAFT_PEERS', '')
        self.peers = peers if peers is not None else [
            p.strip() for p in peers_env.split(',') if _valid(p)
        ]
        raftos.configure({'log_path': f'./logs/{self.node_id or "node"}'})

    async def start(self):
        if not _valid(self.node_id):
            print("[consensus] RAFT_ID not set as host:port; skipping consensus")
            return
        print(f"[consensus] starting as {self.node_id} with peers {self.peers}")
        await raftos.register(self.node_id, self.peers)

    def run(self):
        asyncio.run(self.start())
