from .zone.zone import Zone
from .connection.connection import Connection
from .network_object import NetworkObject
from functools import singledispatchmethod


class Network:
    def __init__(self) -> None:
        self.nb_drones: int | None = None
        self.start_hub: Zone = None
        self.end_hub: Zone = None
        self.zones: list[Zone] = []
        self.connections: list[Connection] = []

    def set_nb_drones(self, nb_drones: int) -> None:
        if self.nb_drones is None:
            self.nb_drones = nb_drones
        else:
            raise ValueError("nb_drones can be declared only once.")

    def set_start_hub(self, start_hub: Zone) -> None:
        if self.start_hub is None:
            self.start_hub = start_hub
        else:
            raise ValueError("start_hub can be declared only once.")

    def set_end_hub(self, end_hub: Zone) -> None:
        if self.end_hub is None:
            self.end_hub = end_hub
        else:
            raise ValueError("end_hub can be declared only once.")

    @singledispatchmethod
    def add_object(self, network_object: NetworkObject) -> None:
        raise ValueError("Unknown object added to Network")

    @add_object.register
    def _(self, network_object: Zone) -> None:
        self.add_zone(network_object)

    @add_object.register
    def _(self, network_object: Connection) -> None:
        self.add_connection(network_object)

    def add_zone(self, zone: Zone) -> None:
        self.zones.append(zone)

    def add_connection(self, connection: Connection) -> None:
        self.connections.append(connection)
