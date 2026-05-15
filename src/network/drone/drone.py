"""Drone entity representing delivery units in the network."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..connection.connection import Connection
    from ..zone.zone import Zone


class Drone():
    """Representation of a drone in the network.

    Drones move through zones and connections carrying cargo.

    Parameters
    ----------
    id : str
        Unique identifier for the drone.
    """
    def __init__(self, id: str) -> None:
        """Initialize a drone.

        Parameters
        ----------
        id : str
            Unique identifier for the drone (e.g., 'D0', 'D1').
        """
        self.id: str = id
        self.zone_by_step: dict[int, 'Zone'] = {}
        self.connection_by_step: dict[int, 'Connection'] = {}
