from src.network.network_object import NetworkObject


class Drone(NetworkObject):
    def __init__(self, id: str) -> None:
        self.id: str = id
