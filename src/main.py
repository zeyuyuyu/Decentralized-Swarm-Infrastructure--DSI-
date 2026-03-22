import os
import time
import random
import asyncio
from typing import List

from dsi.swarm import Swarm
from dsi.node import Node
from dsi.task import Task

class DecentralizedSwarmOrchestrator:
    def __init__(self, swarm_size: int = 10, task_queue_size: int = 100):
        self.swarm = Swarm(size=swarm_size)
        self.task_queue: List[Task] = []
        self.task_queue_size = task_queue_size

    async def run(self):
        while True:
            # Check for new tasks
            self.check_for_new_tasks()

            # Assign tasks to available nodes
            await self.assign_tasks_to_nodes()

            # Monitor node status and reallocate tasks if needed
            await self.monitor_nodes()

            # Wait before checking again
            await asyncio.sleep(1)

    def check_for_new_tasks(self):
        # Simulate new tasks being added to the queue
        new_tasks = [Task(f'Task {i}', random.randint(1, 10)) for i in range(random.randint(1, 5))]
        self.task_queue.extend(new_tasks)

        # Trim the queue if it gets too large
        if len(self.task_queue) > self.task_queue_size:
            self.task_queue = self.task_queue[:self.task_queue_size]

    async def assign_tasks_to_nodes(self):
        # Find available nodes
        available_nodes = [node for node in self.swarm.nodes if not node.is_busy()]

        # Assign tasks to available nodes
        for task in self.task_queue:
            if available_nodes:
                node = available_nodes.pop(0)
                await node.execute_task(task)
                self.task_queue.remove(task)

    async def monitor_nodes(self):
        # Check node status and reallocate tasks if needed
        for node in self.swarm.nodes:
            if node.is_failed():
                # Reallocate tasks from failed node to available nodes
                failed_tasks = node.get_failed_tasks()
                available_nodes = [n for n in self.swarm.nodes if not n.is_busy()]
                for task in failed_tasks:
                    if available_nodes:
                        new_node = available_nodes.pop(0)
                        await new_node.execute_task(task)

if __name__ == '__main__':
    orchestrator = DecentralizedSwarmOrchestrator()
    asyncio.run(orchestrator.run())