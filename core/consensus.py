# core/consensus.py
import os
import asyncio
import raftos

class Consensus:
    """
    Wraps a Raft node (via raftos) for distributed state consensus.
    """
    def __init__(self, node_id=None, peers=None):
        self.node_id = node_id or os.getenv('RAFT_ID', 'node1')
        peer_str = os.getenv('RAFT_PEERS', '')
        self.peers = peers if peers is not None else peer_str.split(',')
        # configure raftos log directory
        raftos.configure({
            'log_path': f'./logs/{self.node_id}'
        })

    async def start(self):
        """
        Registers this node and participates in leader election.
        """
        await raftos.register(self.node_id, self.peers)

    def run(self):
        """
        Launch the asyncio loop for the raft node.
        """
        asyncio.run(self.start())
