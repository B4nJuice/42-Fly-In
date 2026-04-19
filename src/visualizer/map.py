from .tile import Tile
from ..network.coords import Coords


class Map:
    def __init__(self, max_x: int, max_y: int, min_x: int, min_y: int) -> None:
        self.max_x: int = max_x
        self.max_y: int = max_y
        self.min_x: int = min_x
        self.min_y: int = min_y

        self.map: list[list[Tile]]

    def normalize_coords(self, x: int, y: int) -> tuple[int]:
        return (x - self.min_x, y - self.min_y)

    def create_map(self) -> None:
        self.map = [
            [
                Tile(
                    Coords(*self.normalize_coords(x, y))
                )
                for x in range(self.min_x, self.max_x + 1)
            ]
            for y in range(self.min_y, self.max_y + 1)
        ]
