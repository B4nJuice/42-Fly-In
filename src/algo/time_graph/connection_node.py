"""Connection node in the time-expanded graph."""
from .node import Node
from src.network.connection.connection import Connection
from src.network.zone.zone import Zone


class ConnectionNode(Node):
    """Node representing movement along connection in time-expanded graph.

    Parameters
    ----------
    time : int
        The time step this node represents.
    real_node : Zone
        The destination zone of this connection.
    """
    def __init__(self, time: int, real_node: Zone) -> None:
        """Initialize a connection node.

        Parameters
        ----------
        time : int
            The time step.
        real_node : Zone
            The destination zone.
        """
        self.time: int = time
        self.real_node: Zone = real_node
        self.connections: list[tuple[
            'Node' | 'ConnectionNode', Connection | None
                                    ]] = []
