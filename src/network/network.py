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
        if not self.get_zone_by_name(zone.name):
            self.zones.append(zone)
        else:
            raise ValueError(f"multiple declaration for zone {zone.name}")

    def add_connection(self, connection: Connection) -> None:
        self.connections.append(connection)

    def get_zone_by_name(self, name: str) -> Zone | None:
        for zone in self.zones:
            if zone.name == name:
                return zone

        return None

    def process_connections(self) -> None:
        from ..parser.parser import FormatError
        for connection in self.connections:
            try:
                zone1_name, zone2_name = connection.raw_connection.split(
                        "-", maxsplit=1
                    )
            except Exception:
                raise FormatError("incorrect format, "
                                  "format = <zone1-zone2> [metadata].")
            zone1, zone2 = (
                        self.get_zone_by_name(zone1_name),
                        self.get_zone_by_name(zone2_name)
                    )

            if not all([zone1, zone2]):
                raise ValueError(
                        f"unknown zone names {connection.raw_connection}"
                    )

            if zone1_name == zone2_name:
                raise ValueError(
                    f"invalid connection '{connection.raw_connection}':"
                    " duplicate zone."
                    )

            zone1.add_connection(connection)
            zone2.add_connection(connection)

            connection.set_zones(zone1, zone2)

    def verify_zones(self) -> None:
        coords_dict: dict[str, list[Zone]] = {}
        for zone in self.zones:
            coords_dict.setdefault(zone.coords.raw, []).append(zone)

        for c, z in coords_dict.items():
            print(c, " ".join(zo.name for zo in z))
            if len(z) > 1:
                raise ValueError(f"multiple zone on same coords {c}")

    def verify(self) -> None:
        self.process_connections()
        self.verify_zones()
