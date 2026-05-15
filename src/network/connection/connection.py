"""Connection entity representing links between zones in the network."""
from ..network_object import NetworkObject
from ..metadata.connection_metadata import ConnectionMetadata
from ..drone.drone import Drone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..zone.zone import Zone


class Connection(NetworkObject):
    """Represents a connection between two zones in the network.

    Connections allow drones to move between zones with configurable capacity.

    Parameters
    ----------
    name : str
        The name identifier of the connection.
    metadata : ConnectionMetadata
        Connection metadata including capacity constraints.
    """
    def __init__(
                self,
                name: str,
                metadata: ConnectionMetadata
            ) -> None:
        """Initialize a connection.

        Parameters
        ----------
        name : str
            The name identifier of the connection.
        metadata : ConnectionMetadata
            Connection metadata with capacity and other constraints.
        """
        self.name: str = name
        self.metadata: ConnectionMetadata = metadata
        self.zone1: 'Zone' | None = None
        self.zone2: 'Zone' | None = None
        self.drones: list[Drone] = []

    def set_zones(self, zone1: 'Zone', zone2: 'Zone') -> None:
        """Set the two zones this connection links.

        Parameters
        ----------
        zone1 : Zone
            The first zone.
        zone2 : Zone
            The second zone.
        """
        self.zone1 = zone1
        self.zone2 = zone2

    def get_zone_1(self) -> 'Zone':
        """Get the first zone of the connection.

        Returns
        -------
        Zone
            The first zone.

        Raises
        ------
        Exception
            If zone1 has not been set.
        """
        if not self.zone1:
            raise Exception("connection.zone1 has to be set.")
        return self.zone1

    def get_zone_2(self) -> 'Zone':
        """Get the second zone of the connection.

        Returns
        -------
        Zone
            The second zone.

        Raises
        ------
        Exception
            If zone2 has not been set.
        """
        if not self.zone2:
            raise Exception("connection.zone2 has to be set.")
        return self.zone2
