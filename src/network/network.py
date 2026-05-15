"""Network model representing the drone delivery system."""
from .zone.zone import Zone
from .connection.connection import Connection
from .network_object import NetworkObject
from .drone.drone import Drone

from functools import singledispatchmethod
from typing import cast


class Network:
    """Main network model for the drone delivery system.

    The network contains zones (locations), connections (links between zones),
    and drones that move through the network.
    """
    def __init__(self) -> None:
        """Initialize an empty network."""
        self.nb_drones: int = -1
        self.start_hub: Zone | None = None
        self.end_hub: Zone | None = None
        self.zones: list[Zone] = []
        self.connections: list[Connection] = []
        self.drones: list[Drone] = []
        self.max_frames: int = 0
        self.zone_drones_by_step: dict[int, dict[Zone, list[Drone]]] = {}
        self.connection_drones_by_step: dict[
            int,
            dict[Connection, list[Drone]]
        ] = {}

    def get_start_hub(self) -> Zone:
        """Get the start hub zone.

        Returns
        -------
        Zone
            The start hub zone.

        Raises
        ------
        Exception
            If start_hub has not been set.
        """
        if self.start_hub is None:
            raise Exception("start_hub has not been declared")
        return self.start_hub

    def get_end_hub(self) -> Zone:
        """Get the end hub zone.

        Returns
        -------
        Zone
            The end hub zone.

        Raises
        ------
        Exception
            If end_hub has not been set.
        """
        if self.end_hub is None:
            raise Exception("end_hub has not been declared")
        return self.end_hub

    def create_all_drones(self) -> None:
        """Create all drones and place them at the start hub.

        The number of drones must be set first using set_nb_drones().
        """
        for _ in range(self.nb_drones):
            self.create_drone()

        self.set_state_history(
            {0: {self.get_start_hub(): list(self.drones)}},
            {0: {}}
        )

    def create_drone(self) -> None:
        """Create a single drone and place it at the start hub."""
        new_drone: Drone = Drone(f"D{len(self.drones)}")
        self.drones.append(new_drone)
        start = self.get_start_hub()
        start.drones.append(new_drone)
        new_drone.zone_by_step[0] = start

    def set_nb_drones(self, nb_drones: int) -> None:
        """Set the number of drones in the network.

        Parameters
        ----------
        nb_drones : int
            The number of drones to create.

        Raises
        ------
        ValueError
            If nb_drones is not positive or if already set.
        """
        if nb_drones <= 0:
            raise ValueError("nb_drones has to be a positive integer.")
        if self.nb_drones == -1:
            self.nb_drones = nb_drones
        else:
            raise ValueError("nb_drones can be declared only once.")

    def set_start_hub(self, start_hub: Zone) -> None:
        """Set the start hub zone.

        Parameters
        ----------
        start_hub : Zone
            The zone to be marked as start hub.

        Raises
        ------
        ValueError
            If start_hub is already set.
        """
        if self.start_hub is None:
            self.start_hub = start_hub
            start_hub.metadata.set_start_hub()
            start_hub.metadata.metadata.update({"max_drones": self.nb_drones})
        else:
            raise ValueError("start_hub can be declared only once.")

    def set_end_hub(self, end_hub: Zone) -> None:
        """Set the end hub zone.

        Parameters
        ----------
        end_hub : Zone
            The zone to be marked as end hub.

        Raises
        ------
        ValueError
            If end_hub is already set.
        """
        if self.end_hub is None:
            self.end_hub = end_hub
            end_hub.metadata.set_end_hub()
            end_hub.metadata.metadata.update({"max_drones": self.nb_drones})
        else:
            raise ValueError("end_hub can be declared only once.")

    @singledispatchmethod
    def add_object(self, network_object: NetworkObject) -> None:
        """Add a network object (zone or connection).

        Parameters
        ----------
        network_object : NetworkObject
            The object to add (must be Zone or Connection).

        Raises
        ------
        ValueError
            If the object type is not recognized.
        """
        raise ValueError("Unknown object added to Network")

    @add_object.register
    def _(self, network_object: Zone) -> None:
        """Add a zone to the network.

        Parameters
        ----------
        network_object : Zone
            The zone to add.
        """
        self.add_zone(network_object)

    @add_object.register
    def _(self, network_object: Connection) -> None:
        """Add a connection to the network.

        Parameters
        ----------
        network_object : Connection
            The connection to add.
        """
        self.add_connection(network_object)

    def add_zone(self, zone: Zone) -> None:
        """Add a zone to the network.

        Parameters
        ----------
        zone : Zone
            The zone to add.

        Raises
        ------
        ValueError
            If a zone with the same name already exists.
        """
        if not self.get_zone_by_name(zone.name):
            self.zones.append(zone)
        else:
            raise ValueError(f"multiple declaration for zone {zone.name}")

    def add_connection(self, connection: Connection) -> None:
        """Add a connection to the network.

        Parameters
        ----------
        connection : Connection
            The connection to add.
        """
        self.connections.append(connection)

    def get_zone_by_name(self, name: str) -> Zone | None:
        """Get a zone by its name.

        Parameters
        ----------
        name : str
            The zone name to search for.

        Returns
        -------
        Zone | None
            The zone if found, None otherwise.
        """
        for zone in self.zones:
            if zone.name == name:
                return zone
        return None

    def process_connections(self) -> None:
        """Process all connections to link them with their zones.

        Raises
        ------
        FormatError
            If connection name format is invalid.
        ValueError
            If referenced zones don't exist or are identical.
        """
        from ..parser.parser import FormatError
        for connection in self.connections:
            try:
                zone1_name, zone2_name = connection.name.split(
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
                        f"unknown zone names {connection.name}"
                    )

            if zone1_name == zone2_name:
                raise ValueError(
                    f"invalid connection '{connection.name}':"
                    " duplicate zone."
                    )

            cast(Zone, zone1).add_connection(connection)
            cast(Zone, zone2).add_connection(connection)

            connection.set_zones(cast(Zone, zone1), cast(Zone, zone2))

    def verify_zones(self) -> None:
        """Verify all zone metadata is valid."""
        for zone in self.zones:
            zone.metadata.verify_metadata()

    def verify_connections(self) -> None:
        """Verify all connection metadata and uniqueness is valid.

        Raises
        ------
        ValueError
            If duplicate connections between same zones exist.
        """
        connections_dict: dict[str, list[Connection]] = {}

        for c in self.connections:
            c.metadata.verify_metadata()
            name_list: list[str] = [c.get_zone_1().name, c.get_zone_2().name]
            name_list.sort()
            sorted_raw_zones: str = "-".join(name_list)
            connections_dict.setdefault(sorted_raw_zones, []).append(c)

        for s, c_list in connections_dict.items():
            if len(c_list) > 1:
                raise ValueError(f"multiple connection for same zones '{s}'")

    def verify(self) -> None:
        """Verify the complete network structure.

        Processes connections and verifies all zones and connections.
        """
        self.process_connections()
        self.verify_zones()
        self.verify_connections()

    def clear_live_drones(self) -> None:
        """Clear all drones from zones and connections."""
        for zone in self.zones:
            zone.drones = []

        for connection in self.connections:
            connection.drones = []

    def set_state_history(
                self,
                zone_drones_by_step: dict[int, dict[Zone, list[Drone]]],
                connection_drones_by_step: dict[
                    int,
                    dict[Connection, list[Drone]]
                ]
            ) -> None:
        """Set the history of drone positions over time steps.

        Parameters
        ----------
        zone_drones_by_step : dict[int, dict[Zone, list[Drone]]]
            Mapping of step to zone positions with their drones.
        connection_drones_by_step : dict[int, dict[Connection, list[Drone]]]
            Mapping of step to connection positions with their drones.
        """
        self.zone_drones_by_step = zone_drones_by_step
        self.connection_drones_by_step = connection_drones_by_step

        known_steps: set[int] = set(zone_drones_by_step.keys())
        known_steps.update(connection_drones_by_step.keys())
        self.max_frames = max(known_steps, default=0)

        self.apply_state_at_step(0)

    def apply_state_at_step(self, step: int) -> None:
        """Apply the drone state for a specific time step.

        Parameters
        ----------
        step : int
            The time step to apply (clamped to [0, max_frames]).
        """
        self.clear_live_drones()

        clamped_step = min(self.max_frames, max(0, step))

        for zone, drones in self.zone_drones_by_step.get(
                    clamped_step, {}
                ).items():
            zone.drones = list(drones)

        for connection, drones in self.connection_drones_by_step.get(
                    clamped_step,
                    {}
                ).items():
            connection.drones = list(drones)

    def get_state_at_step(self, step: int) -> dict[str, dict[str, list[str]]]:
        """Get the string representation of drone state at a time step.

        Parameters
        ----------
        step : int
            The time step to query (clamped to [0, max_frames]).

        Returns
        -------
        dict[str, dict[str, list[str]]]
            Dictionary with 'zones' and 'connections' keys, each containing
            mappings of location names to lists of drone IDs.
        """
        clamped_step = min(self.max_frames, max(0, step))

        zone_state: dict[str, list[str]] = {
            zone.name: [drone.id for drone in drones]
            for zone, drones in self.zone_drones_by_step.get(
                    clamped_step, {}
                ).items()
        }
        connection_state: dict[str, list[str]] = {
            connection.name: [drone.id for drone in drones]
            for connection, drones in self.connection_drones_by_step.get(
                clamped_step,
                {}
            ).items()
        }

        return {
            "zones": zone_state,
            "connections": connection_state,
        }
