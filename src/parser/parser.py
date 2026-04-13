from ..network.network_object import NetworkObject
from ..network.zone.zone import Zone
from ..network.connection.connection import Connection
from ..network.metadata.zone_metadata import ZoneMetadata
from ..network.metadata.connection_metadata import ConnectionMetadata
from ..network.coords import Coords
from ..network.network import Network


class FormatError(Exception):
    def __init__(self, message: str):
        super().__init__(f"Format Error: {message}")


class Parser:
    def __init__(self, file_path: str) -> None:
        self.file_path: str = file_path
        self.lines: list[str] = self.clean_lines()
        self.network = Network()

    @staticmethod
    def erase_comment(line: str):
        return line.split("#")[0].strip()

    def clean_lines(self) -> list[str]:
        lines: list[str] = []
        clean_lines: list[str] = []

        with open(self.file_path, "r") as opened_file:
            lines = opened_file.readlines()

        clean_lines: list[str] = [
            clean_line
            for line in lines if (clean_line := self.erase_comment(line))
        ]

        return clean_lines

    def split_line(self, line) -> tuple[str, str]:
        splitted_line: list[str] = line.split(":", 1)

        if len(splitted_line) != 2:
            raise FormatError(
                    f"missing key or value (format = key: value) on {line}"
                )

        return tuple(splitted_line)

    def get_object(self, splitted_line: tuple[str, str]) -> NetworkObject:
        key, value = splitted_line
        key = key.strip()
        network_object: NetworkObject | None = None
        datas: list[str] = value.strip()

        match key:
            case "nb_drones":
                self.network.set_nb_drones(int(value))

            case "hub" | "start_hub" | "end_hub":
                datas = datas.split(maxsplit=3)
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

                network_object = Zone(name, coords, metadata)

                if key == "start_hub":
                    self.network.set_start_hub(network_object)
                elif key == "end_hub":
                    self.network.set_end_hub(network_object)

            case "connection":
                datas = datas.split(maxsplit=1)
                raw_connection: str = ""
                metadata: ZoneMetadata | None = None

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

                network_object = Connection(raw_connection, metadata)

            case _:
                raise FormatError(f"Unreconized key: {key}.")

        return network_object

    def parse_map(self) -> Network:
        for line in self.lines:
            network_object: NetworkObject = self.get_object(
                    self.split_line(line)
                )
            if network_object:
                self.network.add_object(network_object)


if __name__ == "__main__":
    parser = Parser("./map.txt")
    parser.parse_map()
    # print(parser.network.nb_drones)
    print(list(map(lambda x: x.metadata.verify_metadata(), parser.network.zones)))
    print("\n".join(list(map(lambda x: f"{x.name} {x.metadata.metadata}", parser.network.zones))))
    print()
    print("\n".join(list(map(lambda x: f"{x.raw_connection} {x.metadata.metadata}", parser.network.connections))))