"""BFS algorithm for finding paths in the time-expanded graph."""
from src.algo.time_graph.time_graph import TimeGraph
from src.algo.time_graph.node import Node
from src.network.connection.connection import Connection
from .bfs_node import BFSNode
from .bfs_edge import BFSEdge
from functools import lru_cache
from typing import cast


class BFS:
    """Breadth-first search for path finding in the network.

    Parameters
    ----------
    time_graph : TimeGraph
        The time-expanded graph to search on.
    """
    def __init__(self, time_graph: TimeGraph) -> None:
        """Initialize BFS with a time-expanded graph.

        Parameters
        ----------
        time_graph : TimeGraph
            The search graph.
        """
        self.time_graph: TimeGraph = time_graph
        self.start_node: BFSNode = cast(BFSNode, self.create_bfs_node(
                list(
                    cast(set[Node], self.time_graph.step_dict.get(0))
                )[0],
                0
            ))

        self.search_edges(self.start_node)
        self.bfs_level: dict[int, set[BFSNode]] = {0: set([self.start_node])}
        self.actual_level: int = 0

        self.end_reached: bool = (
                self.start_node.node.real_node.metadata.end_hub
            )

    def next_level(self) -> None:
        """Expand BFS to the next level."""
        current_level_nodes = list(self.bfs_level.get(self.actual_level, []))
        if not current_level_nodes:
            return

        for node in current_level_nodes:
            if not self.end_reached:
                if node.node.real_node.metadata.end_hub:
                    self.end_reached = True
            for n in node.get_connected_nodes():
                self.bfs_level.setdefault(self.actual_level + 1, set()).add(n)

        self.actual_level += 1

        for node in self.bfs_level.get(self.actual_level, []):
            self.search_edges(node)

    def search_edges(self, node: BFSNode) -> None:
        """Search for edges from a node to future nodes.

        Parameters
        ----------
        node : BFSNode
            The node to search from.
        """
        for node2, connection in node.node.connections:
            if node2.time <= node.node.time:
                continue
            new_node: BFSNode | None =\
                self.create_bfs_node(node2, node.level + 1)

            if new_node:
                if any(edge.node2 == new_node for edge in node.edges):
                    continue

                edge: BFSEdge | None = self.create_bfs_edge(
                        node,
                        new_node,
                        connection
                    )

                if edge:
                    node.edges.append(edge)

    def grow_with_time_step(self) -> None:
        """Grow the search graph by advancing time by one step."""
        self.time_graph.next_step()

        max_known_level: int = max(self.bfs_level.keys(), default=0)

        for level in range(max_known_level + 1):
            for node in self.bfs_level.get(level, set()):
                self.search_edges(node)

        if not self.bfs_level.get(self.actual_level, set()):
            for level in range(self.actual_level - 1, -1, -1):
                if self.bfs_level.get(level, set()):
                    self.actual_level = level
                    break

        self.next_level()

    @lru_cache(maxsize=None)
    def create_bfs_node(self, node: Node, level: int) -> BFSNode | None:
        """Create a BFS node if the zone has positive capacity.

        Parameters
        ----------
        node : Node
            The time-graph node to convert.
        level : int
            The BFS level.

        Returns
        -------
        BFSNode | None
            A new BFS node, or None if capacity is non-positive.
        """
        capacity: int = cast(int, node.real_node.metadata.metadata.get(
                "max_drones"
            ))

        if capacity <= 0:
            return None

        return BFSNode(node, level, capacity)

    def create_bfs_edge(
                self,
                node1: BFSNode,
                node2: BFSNode,
                real_connection: Connection | None
            ) -> BFSEdge | None:
        """Create a BFS edge if it has positive capacity.

        Parameters
        ----------
        node1 : BFSNode
            Source BFS node.
        node2 : BFSNode
            Destination BFS node.
        real_connection : Connection | None
            The network connection, if any.

        Returns
        -------
        BFSEdge | None
            A new BFS edge, or None if capacity is non-positive.
        """
        capacity: int = 0

        if real_connection is None:
            capacity = node1.capacity

        else:
            capacity = cast(int, real_connection.metadata.metadata.get(
                    "max_link_capacity"
                ))

        if capacity <= 0:
            return None

        return BFSEdge(node1, node2, capacity, real_connection)
