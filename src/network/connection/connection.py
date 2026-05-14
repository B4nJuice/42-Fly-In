from ..network_object import NetworkObject
from ..metadata.connection_metadata import ConnectionMetadata
from ..drone.drone import Drone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..zone.zone import Zone


class Connection(NetworkObject):
    def __init__(
                self,
                name: str,
                metadata: ConnectionMetadata
            ) -> None:
        self.name: str = name
        self.metadata: ConnectionMetadata = metadata
        self.zone1: 'Zone' | None = None
        self.zone2: 'Zone' | None = None
        self.drones: list[Drone] = []

    def set_zones(self, zone1: 'Zone', zone2: 'Zone') -> None:
        self.zone1 = zone1
        self.zone2 = zone2
