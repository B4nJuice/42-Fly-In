from src.algo.time_graph.node import Node


class BFSNode:
    def __init__(self, node: Node, level: int, capacity: int) -> None:
        from .bfs_edge import BFSEdge

        self.node: Node = node
        self.level: int = level
        self.capacity: int = capacity
        self.edges: list[BFSEdge] = []
