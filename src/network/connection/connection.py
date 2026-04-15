from ..network_object import NetworkObject
from ..metadata.connection_metadata import ConnectionMetadata


class Connection(NetworkObject):
    def __init__(
                self,
                raw_connection: str,
                metadata: ConnectionMetadata
            ) -> None:
        self.raw_connection: str = raw_connection
        self.metadata: ConnectionMetadata = metadata
        self.zone1: NetworkObject | None = None
        self.zone2: NetworkObject | None = None

    def set_zones(self, zone1: NetworkObject, zone2: NetworkObject) -> None:
        self.zone1 = zone1
        self.zone2 = zone2
