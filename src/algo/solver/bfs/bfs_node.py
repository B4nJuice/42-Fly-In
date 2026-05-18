"""BFS node representation for breadth-first search."""
from src.algo.time_graph.node import Node
from src.network.metadata.zone_metadata import ZoneType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .bfs_edge import BFSEdge


class BFSNode:
    """A node in the breadth-first search graph.

    Parameters
    ----------
    node : Node
        The corresponding time-graph node.
    level : int
        The BFS level (distance from start).
    capacity : int
        Maximum number of drones that can pass through this node.
    """
    def __init__(self, node: Node, level: int, capacity: int) -> None:
        """Initialize a BFS node.

        Parameters
        ----------
        node : Node
            The time-graph node this BFS node represents.
        level : int
            The BFS level.
        capacity : int
            The capacity constraint.
        """

        self.node: Node = node
        self.level: int = level
        self.capacity: int = capacity
        self.passage: int = 0
        self.edges: list['BFSEdge'] = []
        self._edges_ids_hash: list['BFSEdge'] = []

    def get_connected_nodes(self) -> list['BFSNode']:
        """Get all nodes connected from this node.

        Returns
        -------
        list[BFSNode]
            List of connected BFS nodes via outgoing edges.
        """
        return [edge.node2 for edge in self.edges]

    def get_remaining_capacity(self) -> int:
        """Get the remaining available capacity at this node.

        Returns
        -------
        int
            Remaining capacity = total capacity - current passage.
        """
        return self.capacity - self.passage

    def sort_edges(self) -> list['BFSEdge']:
        """Sort edges by priority (non-priority zones first).

        Returns
        -------
        list[Any]
            Sorted edge list, cached when edge set is unchanged.
        """

        if self._edges_ids_hash == self.edges:
            return self.edges

        def has_priority_zone(edge: 'BFSEdge') -> bool:
            real_node = edge.node2.node.real_node
            zone_type = real_node.metadata.metadata.get("zone")
            return zone_type != ZoneType.PRIORITY

        self.edges.sort(key=has_priority_zone)

        self._edges_ids_hash = self.edges

        return self.edges
