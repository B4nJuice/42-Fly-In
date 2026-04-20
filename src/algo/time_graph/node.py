from src.network.network_object import NetworkObject
from typing import Self
from src.network.connection.connection import Connection


class Node:
    def __init__(self, time: int, real_node: NetworkObject) -> None:
        self.time: int = time
        self.real_node: NetworkObject = real_node
        self.connections: list[list[Self, Connection]] = []

    def add_connection(self, node: Self, connection: Connection = None):
        self.connections.append((node, connection))
