"""Map grid for visualization."""
from .tile import Tile
from ..network.coords import Coords


class Map:
    """A 2D grid of tiles for network visualization.

    Parameters
    ----------
    max_x : int
        Maximum X coordinate in the network.
    max_y : int
        Maximum Y coordinate in the network.
    min_x : int
        Minimum X coordinate in the network.
    min_y : int
        Minimum Y coordinate in the network.
    """
    def __init__(self, max_x: int, max_y: int, min_x: int, min_y: int) -> None:
        """Initialize a visualization map.

        Parameters
        ----------
        max_x : int
            Maximum X coordinate.
        max_y : int
            Maximum Y coordinate.
        min_x : int
            Minimum X coordinate.
        min_y : int
            Minimum Y coordinate.
        """
        self.max_x: int = max_x
        self.max_y: int = max_y
        self.min_x: int = min_x
        self.min_y: int = min_y

        self.map: list[list[Tile]]

    def normalize_coords(self, x: int, y: int) -> tuple[int, int]:
        """Convert network coordinates to map tile indices.

        Parameters
        ----------
        x : int
            Network X coordinate.
        y : int
            Network Y coordinate.

        Returns
        -------
        tuple[int, int]
            Normalized (tile_x, tile_y) coordinates.
        """
        return (x - self.min_x, y - self.min_y)

    def create_map(self) -> None:
        """Create the 2D grid of tiles based on network bounds."""
        self.map = [
            [
                Tile(
                    Coords(*self.normalize_coords(x, y))
                )
                for x in range(self.min_x, self.max_x + 1)
            ]
            for y in range(self.min_y, self.max_y + 1)
        ]
