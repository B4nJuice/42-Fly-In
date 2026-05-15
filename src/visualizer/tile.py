"""Tile representation for the visualization grid."""
from ..network.coords import Coords
from ..network.zone.zone import Zone
from ..network.connection.connection import Connection


class Tile:
    """A single tile in the visualization grid.

    Parameters
    ----------
    coords : Coords
        The 2D coordinates of this tile.
    """
    def __init__(self, coords: Coords) -> None:
        """Initialize a tile.

        Parameters
        ----------
        coords : Coords
            The tile coordinates.
        """
        self.coords: Coords = coords
        self.objects: list[Zone | Connection] = []

    def add_object(self, _object: Zone | Connection) -> None:
        """Add a zone or connection object to this tile.

        Parameters
        ----------
        _object : Zone | Connection
            The network object to add.
        """
        self.objects.append(_object)
