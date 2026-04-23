from src.algo.time_graph.node import Node
from src.network.metadata.zone_metadata import ZoneType
from typing import Any


class BFSNode:
    def __init__(self, node: Node, level: int, capacity: int) -> None:
        from .bfs_edge import BFSEdge

        self.node: Node = node
        self.level: int = level
        self.capacity: int = capacity
        self.passage: int = 0
        self.edges: list[BFSEdge] = []
        self._edges_ids_hash = None

    def get_connected_nodes(self) -> list['BFSNode']:
        return [edge.node2 for edge in self.edges]

    def get_remaining_capacity(self) -> int:
        return self.capacity - self.passage

    def sort_edges(self) -> list[Any]:
        current_edges_ids = tuple(id(edge) for edge in self.edges)

        if self._edges_ids_hash == current_edges_ids:
            return self.edges

        def has_priority_zone(edge) -> bool:
            real_node = edge.node2.node.real_node
            zone_type = real_node.metadata.metadata.get("zone")
            return zone_type != ZoneType.PRIORITY

        self.edges.sort(key=has_priority_zone)

        self._edges_ids_hash = current_edges_ids

        return self.edges
