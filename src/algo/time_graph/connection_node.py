from .node import Node
from typing import Self
from src.network.network import NetworkObject
from src.network.connection.connection import Connection


class ConnectionNode(Node):
    def __init__(self, time: int, real_node: NetworkObject) -> None:
        self.time: int = time
        self.real_node: NetworkObject = real_node
        self.connections: list[list[Self, Connection]] = []
