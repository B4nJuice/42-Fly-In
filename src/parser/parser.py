"""Parsing module for loading map configurations from files."""
from typing import Any

from ..network.zone.zone import Zone
from ..network.connection.connection import Connection
from ..network.metadata.zone_metadata import ZoneMetadata
from ..network.metadata.connection_metadata import ConnectionMetadata
from ..network.coords import Coords
from ..network.network import Network
from .config_parser import Config, ConfigError


class FormatError(Exception):
    """Exception raised when map file format is invalid.

    Parameters
    ----------
    message : str
        Description of the format error.
    """
    def __init__(self, message: str):
        """Initialize FormatError with a formatted message.

        Parameters
        ----------
        message : str
            The error message.
        """
        super().__init__(f"Format Error: {message}")


class MapConfig(Config):
    """Configuration parser for map files."""
    @staticmethod
    def get_unprocessed_value(line: str) -> tuple[str, str]:
        """Extract parameter and value from a configuration line.

        Parameters
        ----------
        line : str
            A configuration line in format "parameter: value".

        Returns
        -------
        tuple[str, str]
            A tuple of (parameter, value) with whitespace stripped.

        Raises
        ------
        ConfigError
            If the line format is invalid or parameter is missing.
        """
        if ":" not in line:
            raise ConfigError(f"undefined config line : {line}")

        parameter, value = line.split(":", maxsplit=1)
        parameter = parameter.strip()
        value = value.strip()

        if not parameter:
            raise ConfigError(f"undefined config line : {line}")

        return (parameter, value)


class Parser:
    """Parser for loading network maps from configuration files.

    Parameters
    ----------
    file_path : str
        Path to the map configuration file to parse.
    """
    def __init__(self, file_path: str) -> None:
        """Initialize the parser with a file path.

        Parameters
        ----------
        file_path : str
            Path to the map configuration file.
        """
        self.file_path: str = file_path
        self.network = Network()

    @staticmethod
    def parse_zone(raw_value: str) -> Zone:
        """Parse a zone definition from a string.

        Parameters
        ----------
        raw_value : str
            Zone definition in format "name x y [metadata]".

        Returns
        -------
        Zone
            The parsed zone object.

        Raises
        ------
        FormatError
            If the zone definition format is invalid.
        """
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
        """Parse a connection definition from a string.

        Parameters
        ----------
        raw_value : str
            Connection definition in format "zone1-zone2 [metadata]".

        Returns
        -------
        Connection
            The parsed connection object.

        Raises
        ------
        FormatError
            If the connection definition format is invalid.
        """
        datas = raw_value.strip().split(maxsplit=1)
        name: str = ""
        metadata: ConnectionMetadata | None = None

        match len(datas):
            case 1:
                name = datas[0]
                metadata = ConnectionMetadata("[]")

            case 2:
                name = datas[0]
                metadata = ConnectionMetadata(datas[1])

            case _:
                raise FormatError(
                        "incorrect format, "
                        "format = <zone1-zone2> [metadata]."
                    )

        return Connection(name, metadata)

    @staticmethod
    def to_list(value: Any) -> list[Any]:
        """Convert a value to a list.

        Parameters
        ----------
        value : Any
            The value to convert. None becomes empty list, lists are unchanged.

        Returns
        -------
        list[Any]
            The value as a list.
        """
        if value is None:
            return []
        if isinstance(value, list):
            return value
        return [value]

    def make_config(self) -> MapConfig:
        """Create and configure a MapConfig parser.

        Returns
        -------
        MapConfig
            A configured MapConfig object with parameter specifications.
        """
        config = MapConfig()
        config.add_parameter("nb_drones", [0, [int]])
        config.add_parameter("start_hub", [None, [Parser.parse_zone]])
        config.add_parameter("end_hub", [None, [Parser.parse_zone]])
        config.add_parameter("hub", [[], [Parser.parse_zone]])
        config.add_parameter("connection", [[], [Parser.parse_connection]])
        return config

    def parse_map(self) -> Network:
        """Parse the map file and build the network.

        Returns
        -------
        Network
            The loaded network with all zones and connections.

        Raises
        ------
        ConfigError
            If the map file format is invalid or doesn't start with nb_drones.
        """
        config = self.make_config()

        with open(self.file_path, "r") as opened_file:
            config.parse_file(opened_file)

        if not config.get_lines()[0].startswith("nb_drones"):
            raise ConfigError("map has to start with 'nb_drones'.")

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
