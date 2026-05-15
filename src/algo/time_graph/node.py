"""Time-expanded graph node for temporal pathfinding."""
from src.network.connection.connection import Connection
from src.network.zone.zone import Zone

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .connection_node import ConnectionNode


class Node:
    """A node in the time-expanded graph representing a zone at a time step.

    Parameters
    ----------
    time : int
        The time step this node represents.
    real_node : Zone
        The zone this node corresponds to.
    """
    def __init__(self, time: int, real_node: Zone) -> None:
        """Initialize a time-expanded graph node.

        Parameters
        ----------
        time : int
            The time step.
        real_node : Zone
            The zone at this time.
        """
        self.time: int = time
        self.real_node: Zone = real_node
        self.connections: list[tuple[
            'Node' | 'ConnectionNode', Connection | None
                                    ]] = []

    def add_connection(
                self,
                node: 'Node',
                connection: Connection | None = None
            ) -> None:
        """Add a connection to another node.

        Parameters
        ----------
        node : Node
            The destination node.
        connection : Connection | None, optional
            The network connection, if this is a real connection.
        """
        self.connections.append((node, connection))
