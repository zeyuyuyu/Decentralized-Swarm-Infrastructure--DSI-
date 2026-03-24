import os
import json
import time
import random
import hashlib
import threading

class SwarmNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.ledger = []
        self.pending_transactions = []
        self.neighbors = []
        self.lock = threading.Lock()

    def add_transaction(self, transaction):
        with self.lock:
            self.pending_transactions.append(transaction)

    def propose_block(self):
        with self.lock:
            block = {
                'index': len(self.ledger),
                'timestamp': time.time(),
                'transactions': self.pending_transactions,
                'previous_hash': self.ledger[-1]['hash'] if self.ledger else '0'
            }
            block['hash'] = self.calculate_hash(block)
            self.ledger.append(block)
            self.pending_transactions = []
            return block

    def calculate_hash(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def validate_block(self, block):
        if block['index'] != len(self.ledger):
            return False
        if block['previous_hash'] != (self.ledger[-1]['hash'] if self.ledger else '0'):
            return False
        if block['hash'] != self.calculate_hash(block):
            return False
        return True

    def run_consensus(self):
        while True:
            time.sleep(random.uniform(1, 5))
            block = self.propose_block()
            votes = 0
            for neighbor in self.neighbors:
                if neighbor.validate_block(block):
                    votes += 1
            if votes > len(self.neighbors) // 2:
                for neighbor in self.neighbors:
                    neighbor.add_block(block)

def main():
    nodes = [SwarmNode(f'node_{i}') for i in range(10)]
    for node in nodes:
        node.neighbors = [n for n in nodes if n != node]
    for node in nodes:
        threading.Thread(target=node.run_consensus).start()

if __name__ == '__main__':
    main()