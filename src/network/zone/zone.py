from ..coords import Coords
from ..metadata.zone_metadata import ZoneMetadata
from ..network_object import NetworkObject
from ..drone.drone import Drone
from functools import lru_cache


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
        self.is_special: bool = False
        self.connections: list[NetworkObject] = []
        self.drones: list[Drone] = []

    def add_connection(self, connection: NetworkObject) -> None:
        self.connections.append(connection)

    @lru_cache(maxsize=None)
    def get_connections(self) -> list[tuple[NetworkObject, NetworkObject]]:
        connections: list[tuple[Zone, NetworkObject]] = []

        for connection in self.connections:
            if connection.zone1 is self:
                connections.append((connection.zone2, connection))
            else:
                connections.append((connection.zone1, connection))

        return connections
