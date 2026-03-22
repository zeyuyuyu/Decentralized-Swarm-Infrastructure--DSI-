import os
import json
import time
import random
import requests
from typing import List, Dict

class SwarmOrchestrator:
    def __init__(self, swarm_config_path: str):
        with open(swarm_config_path, 'r') as f:
            self.config = json.load(f)
        self.nodes = self.config['nodes']
        self.replication_factor = self.config['replication_factor']

    def _get_available_nodes(self) -> List[str]:
        available_nodes = []
        for node in self.nodes:
            try:
                response = requests.get(f"http://{node}/health")
                if response.status_code == 200:
                    available_nodes.append(node)
            except requests.exceptions.RequestException:
                continue
        return available_nodes

    def _assign_replicas(self, data: bytes, num_replicas: int) -> Dict[str, bytes]:
        available_nodes = self._get_available_nodes()
        if len(available_nodes) < num_replicas:
            raise ValueError("Not enough available nodes to satisfy replication factor")

        replica_assignments = {}
        for i in range(num_replicas):
            node = random.choice(available_nodes)
            available_nodes.remove(node)
            replica_assignments[node] = data

        return replica_assignments

    def store_data(self, data: bytes) -> None:
        replicas = self._assign_replicas(data, self.replication_factor)
        for node, replica in replicas.items():
            try:
                requests.post(f"http://{node}/store", data=replica)
            except requests.exceptions.RequestException:
                continue

    def retrieve_data(self, key: str) -> bytes:
        available_nodes = self._get_available_nodes()
        if len(available_nodes) < self.replication_factor:
            raise ValueError("Not enough available nodes to satisfy replication factor")

        for node in available_nodes:
            try:
                response = requests.get(f"http://{node}/retrieve?key={key}")
                if response.status_code == 200:
                    return response.content
            except requests.exceptions.RequestException:
                continue

        raise ValueError(f"Could not retrieve data for key: {key}")
