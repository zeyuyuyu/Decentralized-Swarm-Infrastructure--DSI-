# Decentralized Governance Protocol

import random

class GovernanceNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.vote_weight = random.uniform(0.1, 1.0)
        self.vote_history = []

class GovernanceProtocol:
    def __init__(self, num_nodes=10):
        self.nodes = [GovernanceNode(i) for i in range(num_nodes)]
        self.proposal_queue = []

    def submit_proposal(self, proposal):
        self.proposal_queue.append(proposal)

    def vote_on_proposal(self, node, proposal):
        node.vote_history.append(proposal)
        total_weight = sum(n.vote_weight for n in self.nodes)
        if sum(n.vote_weight for n in self.nodes if proposal in n.vote_history) / total_weight > 0.5:
            self.execute_proposal(proposal)

    def execute_proposal(self, proposal):
        print(f"Executing proposal: {proposal}")
        self.proposal_queue.remove(proposal)

if __name__ == "__main__":
    protocol = GovernanceProtocol()
    protocol.submit_proposal("Increase node reward rate")
    for node in protocol.nodes:
        protocol.vote_on_proposal(node, "Increase node reward rate")
