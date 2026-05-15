"""BFS edge representation for breadth-first search."""
from .bfs_node import BFSNode
from src.network.connection.connection import Connection


class BFSEdge:
    """An edge in the breadth-first search graph.

    Connects two BFS nodes with a capacity constraint.

    Parameters
    ----------
    node1 : BFSNode
        The source BFS node.
    node2 : BFSNode
        The destination BFS node.
    capacity : int
        Maximum number of drones that can use this edge.
    real_connection : Connection | None, optional
        The real network connection this edge represents, if any.
    """
    def __init__(
                self,
                node1: BFSNode,
                node2: BFSNode,
                capacity: int,
                real_connection: Connection | None = None
            ) -> None:
        """Initialize a BFS edge.

        Parameters
        ----------
        node1 : BFSNode
            Source node.
        node2 : BFSNode
            Destination node.
        capacity : int
            Edge capacity.
        real_connection : Connection | None, optional
            Associated network connection.
        """
        self.node1: BFSNode = node1
        self.node2: BFSNode = node2
        self.capacity: int = capacity
        self.passage: int = 0
        self.real_connection: Connection | None = real_connection

    def get_remaining_capacity(self) -> int:
        """Get the remaining available capacity on this edge.

        Returns
        -------
        int
            Remaining capacity = total capacity - current passage.
        """
        return self.capacity - self.passage
