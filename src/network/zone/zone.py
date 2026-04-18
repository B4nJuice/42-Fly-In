from ..coords import Coords
from ..metadata.zone_metadata import ZoneMetadata
from ..network_object import NetworkObject


class Zone(NetworkObject):
    def __init__(
                self,
                name: str,
                coords: Coords,
                metadata: ZoneMetadata
            ):
        self.name: str = name
        self.metadata: ZoneMetadata = metadata
        self.coords: Coords = coords
        self.is_special: bool = False
        self.connections: list[NetworkObject] = []

    def add_connection(self, connection: NetworkObject) -> None:
        self.connections.append(connection)
