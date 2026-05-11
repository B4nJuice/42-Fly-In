from .bfs_node import BFSNode
from src.network.connection.connection import Connection


class BFSEdge:
    def __init__(
                self,
                node1: BFSNode,
                node2: BFSNode,
                capacity: int,
                real_connection: Connection | None = None
            ) -> None:
        self.node1: BFSNode = node1
        self.node2: BFSNode = node2
        self.capacity: int = capacity
        self.passage: int = 0
        self.real_connection: Connection | None = real_connection

    def get_remaining_capacity(self) -> int:
        return self.capacity - self.passage
