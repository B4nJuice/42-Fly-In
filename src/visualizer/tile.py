from ..network.coords import Coords
from ..network.network_object import NetworkObject


class Tile:
    def __init__(self, coords: Coords) -> None:
        self.coords: Coords = coords
        self.objects: list[NetworkObject] = []

    def add_object(self, object: NetworkObject) -> None:
        self.objects.append(object)
