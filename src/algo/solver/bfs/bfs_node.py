from src.algo.time_graph.node import Node


class BFSNode:
    def __init__(self, node: Node, level: int, capacity: int) -> None:
        from .bfs_edge import BFSEdge

        self.node: Node = node
        self.level: int = level
        self.capacity: int = capacity
        self.passage: int = 0
        self.edges: list[BFSEdge] = []

    def get_connected_nodes(self) -> list['BFSNode']:
        return [edge.node2 for edge in self.edges]
