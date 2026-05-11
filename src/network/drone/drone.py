from src.network.network_object import NetworkObject


class Drone(NetworkObject):
    def __init__(self, id: str) -> None:
        self.id: str = id
        self.zone_by_step: dict[int, NetworkObject] = {}
        self.connection_by_step: dict[int, NetworkObject] = {}
