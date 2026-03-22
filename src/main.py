import asyncio
import random
import time

class DecentralizedSwarmConsensus:
    def __init__(self, node_count, quorum_size):
        self.node_count = node_count
        self.quorum_size = quorum_size
        self.nodes = [Node(i) for i in range(node_count)]
        self.consensus_state = {}

    async def run_consensus(self):
        while True:
            await asyncio.gather(*[node.propose_update() for node in self.nodes])
            await asyncio.gather(*[node.vote_on_updates() for node in self.nodes])
            await self.tally_votes()
            await asyncio.sleep(random.uniform(1, 5))

    async def tally_votes(self):
        for key, votes in self.consensus_state.items():
            if len(votes) >= self.quorum_size:
                print(f'Consensus reached on key: {key}, value: {max(votes, key=votes.count)}')
                for node in self.nodes:
                    node.consensus_state[key] = max(votes, key=votes.count)
            else:
                print(f'No consensus reached on key: {key}')

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.consensus_state = {}

    async def propose_update(self):
        key = random.choice(list(self.consensus_state.keys()))
        value = random.randint(1, 100)
        self.consensus_state[key] = value
        print(f'Node {self.node_id} proposed update: {key}={value}')

    async def vote_on_updates(self):
        for key, value in self.consensus_state.items():
            if key not in DSI.consensus_state:
                DSI.consensus_state[key] = []
            DSI.consensus_state[key].append(value)

if __name__ == '__main__':
    DSI = DecentralizedSwarmConsensus(node_count=10, quorum_size=6)
    asyncio.run(DSI.run_consensus())