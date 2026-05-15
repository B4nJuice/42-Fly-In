from ..network.coords import Coords
from ..network.zone.zone import Zone
from ..network.connection.connection import Connection


class Tile:
    def __init__(self, coords: Coords) -> None:
        self.coords: Coords = coords
        self.objects: list[Zone | Connection] = []

    def add_object(self, _object: Zone | Connection) -> None:
        self.objects.append(_object)
