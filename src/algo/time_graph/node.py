from src.network.network_object import NetworkObject
from typing import Self


class Node:
    def __init__(self, time: int, real_node: NetworkObject) -> None:
        self.time: int = time
        self.real_node: NetworkObject = real_node
        self.connections: list[Self] = []

    def add_connection(self, node: Self):
        self.connections.append(node)
