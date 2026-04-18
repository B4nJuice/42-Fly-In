from typing import Any

from ..network.zone.zone import Zone
from ..network.connection.connection import Connection
from ..network.metadata.zone_metadata import ZoneMetadata
from ..network.metadata.connection_metadata import ConnectionMetadata
from ..network.coords import Coords
from ..network.network import Network
from .config_parser import Config, ConfigError


class FormatError(Exception):
    def __init__(self, message: str):
        super().__init__(f"Format Error: {message}")


class MapConfig(Config):
    @staticmethod
    def get_unprocessed_value(line: str) -> tuple[str, str]:
        if ":" not in line:
            raise ConfigError(f"undefined config line : {line}")

        parameter, value = line.split(":", maxsplit=1)
        parameter = parameter.strip()
        value = value.strip()

        if not parameter:
            raise ConfigError(f"undefined config line : {line}")

        return (parameter, value)


class Parser:
    def __init__(self, file_path: str) -> None:
        self.file_path: str = file_path
        self.network = Network()

    @staticmethod
    def parse_zone(raw_value: str) -> Zone:
        datas = raw_value.strip().split(maxsplit=3)
        name: str = ""
        coords: Coords = Coords()
        metadata: ZoneMetadata | None = None

        match len(datas):
            case 3:
                name = datas[0]
                coords = Coords(datas[1], datas[2])
                metadata = ZoneMetadata("[]")

            case 4:
                name = datas[0]
                coords = Coords(datas[1], datas[2])
                metadata = ZoneMetadata(datas[3])

            case _:
                raise FormatError(
                        "incorrect format, "
                        "format = <name> <x> <y> [metadata]."
                    )

        return Zone(name, coords, metadata)

    @staticmethod
    def parse_connection(raw_value: str) -> Connection:
        datas = raw_value.strip().split(maxsplit=1)
        raw_connection: str = ""
        metadata: ConnectionMetadata | None = None

        match len(datas):
            case 1:
                raw_connection = datas[0]
                metadata = ConnectionMetadata("[]")

            case 2:
                raw_connection = datas[0]
                metadata = ConnectionMetadata(datas[1])

            case _:
                raise FormatError(
                        "incorrect format, "
                        "format = <zone1-zone2> [metadata]."
                    )

        return Connection(raw_connection, metadata)

    @staticmethod
    def to_list(value: Any) -> list[Any]:
        if value is None:
            return []
        if isinstance(value, list):
            return value
        return [value]

    def make_config(self) -> MapConfig:
        config = MapConfig()
        config.add_parameter("nb_drones", [0, [int]])
        config.add_parameter("start_hub", [None, [Parser.parse_zone]])
        config.add_parameter("end_hub", [None, [Parser.parse_zone]])
        config.add_parameter("hub", [[], [Parser.parse_zone]])
        config.add_parameter("connection", [[], [Parser.parse_connection]])
        return config

    def parse_map(self) -> Network:
        config = self.make_config()

        with open(self.file_path, "r") as opened_file:
            config.parse_file(opened_file)

        for nb_drones in self.to_list(config.get_value("nb_drones")):
            self.network.set_nb_drones(nb_drones)

        for start_hub in self.to_list(config.get_value("start_hub")):
            self.network.add_object(start_hub)
            self.network.set_start_hub(start_hub)

        for end_hub in self.to_list(config.get_value("end_hub")):
            self.network.add_object(end_hub)
            self.network.set_end_hub(end_hub)

        for hub in self.to_list(config.get_value("hub")):
            self.network.add_object(hub)

        for connection in self.to_list(config.get_value("connection")):
            self.network.add_object(connection)

        return self.network


if __name__ == "__main__":
    parser = Parser("./map.txt")
    parser.parse_map()
    parser.network.verify()
    print("OK")
