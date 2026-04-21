from .bfs_node import BFSNode


class BFSEdge:
    def __init__(self, node1: BFSNode, node2: BFSNode, capacity: int) -> None:
        self.node1: BFSNode = node1
        self.node2: BFSNode = node2
        self.capacity: int = capacity
        self.passage: int = 0
