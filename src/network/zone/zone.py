"""Zone entity representing locations in the network."""
from ..coords import Coords
from ..metadata.zone_metadata import ZoneMetadata
from ..network_object import NetworkObject
from ..drone.drone import Drone
from functools import lru_cache
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..connection.connection import Connection


class Zone(NetworkObject):
    """Represents a zone (location) in the network.

    Zones are network nodes where drones can be located and wait.

    Parameters
    ----------
    name : str
        The name identifier of the zone (no dashes allowed).
    coords : Coords
        The 2D coordinates of the zone.
    metadata : ZoneMetadata
        Zone metadata including type, color, and capacity constraints.
    """
    def __init__(
                self,
                name: str,
                coords: Coords,
                metadata: ZoneMetadata
            ) -> None:
        """Initialize a zone.

        Parameters
        ----------
        name : str
            The name identifier of the zone.
        coords : Coords
            The 2D coordinates.
        metadata : ZoneMetadata
            Zone metadata configuration.

        Raises
        ------
        FormatError
            If the zone name contains dashes.
        """
        from src.parser.parser import FormatError
        if name.count("-"):
            raise FormatError(f"{name} contain dash ('-').")

        self.name: str = name
        self.metadata: ZoneMetadata = metadata
        self.coords: Coords = coords
        self.connections: list['Connection'] = []
        self.drones: list[Drone] = []

    def add_connection(self, connection: 'Connection') -> None:
        """Add a connection to this zone.

        Parameters
        ----------
        connection : Connection
            The connection to add.
        """
        self.connections.append(connection)

    @lru_cache(maxsize=None)
    def get_connections(self) -> list[tuple['Zone', 'Connection']]:
        """Get all connected zones and their connections.

        Returns
        -------
        list[tuple[Zone, Connection]]
            List of (connected_zone, connection) tuples.

        Note
        ----
        Results are cached using lru_cache for performance.
        """
        connections: list[tuple['Zone', 'Connection']] = []

        for connection in self.connections:
            if connection.get_zone_1() is self:
                connections.append((connection.get_zone_2(), connection))
            else:
                connections.append((connection.get_zone_1(), connection))

        return connections
