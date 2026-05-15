from ..coords import Coords
from ..metadata.zone_metadata import ZoneMetadata
from ..network_object import NetworkObject
from ..drone.drone import Drone
from functools import lru_cache
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..connection.connection import Connection


class Zone(NetworkObject):
    def __init__(
                self,
                name: str,
                coords: Coords,
                metadata: ZoneMetadata
            ) -> None:

        from src.parser.parser import FormatError
        if name.count("-"):
            raise FormatError(f"{name} contain dash ('-').")

        self.name: str = name
        self.metadata: ZoneMetadata = metadata
        self.coords: Coords = coords
        self.connections: list['Connection'] = []
        self.drones: list[Drone] = []

    def add_connection(self, connection: 'Connection') -> None:
        self.connections.append(connection)

    @lru_cache(maxsize=None)
    def get_connections(self) -> list[tuple['Zone', 'Connection']]:
        connections: list[tuple['Zone', 'Connection']] = []

        for connection in self.connections:
            if connection.get_zone_1() is self:
                connections.append((connection.get_zone_2(), connection))
            else:
                connections.append((connection.get_zone_1(), connection))

        return connections
