from .node import Node
from src.network.connection.connection import Connection
from src.network.zone.zone import Zone


class ConnectionNode(Node):
    def __init__(self, time: int, real_node: Zone) -> None:
        self.time: int = time
        self.real_node: Zone = real_node
        self.connections: list[tuple[
            'Node' | 'ConnectionNode', Connection | None
                                    ]] = []
