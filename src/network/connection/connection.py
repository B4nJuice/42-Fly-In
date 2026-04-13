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
