import os
import json
import time
import random
import multiprocessing as mp

from typing import List, Dict

class SwarmNode:
    def __init__(self, node_id: str, capabilities: List[str]):
        self.node_id = node_id
        self.capabilities = capabilities
        self.load = 0
        self.available = True

class SwarmOrchestrator:
    def __init__(self, nodes: List[SwarmNode]):
        self.nodes = nodes
        self.task_queue: List[Dict] = []
        self.running_tasks: Dict[str, SwarmNode] = {}

    def add_task(self, task: Dict):
        self.task_queue.append(task)

    def allocate_task(self):
        while self.task_queue:
            task = self.task_queue.pop(0)
            capabilities = task['required_capabilities']
            available_nodes = [node for node in self.nodes if node.available and all(cap in node.capabilities for cap in capabilities)]
            if available_nodes:
                node = min(available_nodes, key=lambda n: n.load)
                node.load += 1
                node.available = False
                self.running_tasks[task['id']] = node
                return task
        return None

    def complete_task(self, task_id: str):
        if task_id in self.running_tasks:
            node = self.running_tasks.pop(task_id)
            node.load -= 1
            node.available = True

def simulate_swarm(num_nodes: int, num_tasks: int):
    nodes = [SwarmNode(f'node_{i}', random.sample(['cpu', 'gpu', 'memory', 'storage'], random.randint(1, 4))) for i in range(num_nodes)]
    orchestrator = SwarmOrchestrator(nodes)

    for _ in range(num_tasks):
        task = {
            'id': f'task_{len(orchestrator.task_queue)}',
            'required_capabilities': random.sample(['cpu', 'gpu', 'memory', 'storage'], random.randint(1, 3))
        }
        orchestrator.add_task(task)

    while orchestrator.task_queue or orchestrator.running_tasks:
        task = orchestrator.allocate_task()
        if task:
            print(f'Allocated task {task["id"]} to node {orchestrator.running_tasks[task["id"]].node_id}')
            time.sleep(random.uniform(1, 5))
            orchestrator.complete_task(task['id'])
        else:
            time.sleep(0.1)

if __name__ == '__main__':
    simulate_swarm(10, 20)
