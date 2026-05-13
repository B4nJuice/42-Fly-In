from ..network_object import NetworkObject
from ..metadata.connection_metadata import ConnectionMetadata
from ..drone.drone import Drone


class Connection(NetworkObject):
    def __init__(
                self,
                name: str,
                metadata: ConnectionMetadata
            ) -> None:
        self.name: str = name
        self.metadata: ConnectionMetadata = metadata
        self.zone1: NetworkObject | None = None
        self.zone2: NetworkObject | None = None
        self.drones: [Drone] = []

    def set_zones(self, zone1: NetworkObject, zone2: NetworkObject) -> None:
        self.zone1 = zone1
        self.zone2 = zone2
