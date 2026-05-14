from src.network.connection.connection import Connection
from src.network.zone.zone import Zone

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .connection_node import ConnectionNode


class Node:
    def __init__(self, time: int, real_node: Zone) -> None:
        self.time: int = time
        self.real_node: Zone = real_node
        self.connections: list[tuple[
            'Node' | 'ConnectionNode', Connection | None
                                    ]] = []

    def add_connection(
                self,
                node: 'Node',
                connection: Connection | None = None
            ):
        self.connections.append((node, connection))
