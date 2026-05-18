"""DFS algorithm for finding augmenting paths and computing max flow."""
from ..bfs.bfs import BFS
from ..bfs.bfs_node import BFSNode
from ..bfs.bfs_edge import BFSEdge
from src.algo.time_graph.connection_node import ConnectionNode
from src.network.zone.zone import Zone
from src.network.drone.drone import Drone
from src.network.connection.connection import Connection


class DFS:
    """Depth-first search for finding augmenting paths in the network.

    Uses DFS to find paths from start to end hub, applying flow constraints.

    Parameters
    ----------
    bfs : BFS
        The BFS instance to search on.
    """
    def __init__(self, bfs: BFS) -> None:
        """Initialize DFS with a BFS graph.

        Parameters
        ----------
        bfs : BFS
            The BFS graph to search.
        """
        self.bfs: BFS = bfs
        self.paths: list[list[BFSNode | BFSEdge]] = []

    @staticmethod
    def get_starting_node(path: list[BFSNode | BFSEdge]) -> BFSNode:
        """Get the current node from a path (last element).

        Parameters
        ----------
        path : list[BFSNode | BFSEdge]
            A path (alternating nodes and edges).

        Returns
        -------
        BFSNode
            The last node in the path.

        Raises
        ------
        Exception
            If the last element is an edge instead of a node.
        """
        if isinstance(path[-1], BFSEdge):
            raise Exception("starting_nod has to be a node, not a connection.")

        return path[-1]

    def create_path(
                self,
                path: list[BFSNode | BFSEdge],
                visited: set[BFSNode],
                visited_edges: set[BFSEdge],
                dead_ends: set[BFSNode]
            ) -> list[BFSNode | BFSEdge] | None:
        """Recursively find a path from current node to end hub.

        Parameters
        ----------
        path : list[BFSNode | BFSEdge]
            Current path being explored.
        visited : set[BFSNode]
            Visited nodes in current exploration.
        visited_edges : set[BFSEdge]
            Visited edges in current exploration.
        dead_ends : set[BFSNode]
            Nodes that cannot lead to solution.

        Returns
        -------
        list[BFSNode | BFSEdge] | None
            A complete path if found, None otherwise.
        """
        starting_node: BFSNode = self.get_starting_node(path)

        if starting_node in dead_ends:
            return None

        if starting_node.get_remaining_capacity() <= 0:
            dead_ends.add(starting_node)
            return None

        visited.add(starting_node)

        for edge in starting_node.sort_edges():
            if edge.get_remaining_capacity() > 0 and not (
                        edge in visited_edges
                    ):
                next_edge: BFSEdge = edge

                visited_edges.add(next_edge)

                next_node: BFSNode = next_edge.node1 if (
                        starting_node != next_edge.node1
                    ) else next_edge.node2

                if not (next_node in visited):
                    path_len: int = len(path)

                    path.append(next_edge)
                    path.append(next_node)

                    if next_node.node.real_node.metadata.end_hub:
                        return path

                    new_path: list[BFSNode | BFSEdge] | None =\
                        self.create_path(
                            path, visited, visited_edges, dead_ends
                        )

                    if new_path:
                        return new_path

                    del path[path_len:]
                    visited_edges.discard(next_edge)
                    visited.discard(next_node)

        dead_ends.add(starting_node)
        return None

    def get_all_paths(self) -> int:
        """Compute maximum flow by finding all augmenting paths.

        Returns
        -------
        int
            Total flow (number of paths found).
        """
        max_flow: int = 0

        while max_flow < self.bfs.time_graph.network.nb_drones:
            path = self.create_path([self.bfs.start_node], set(), set(), set())

            if not path:
                self.bfs.grow_with_time_step()
                continue

            flow: int = self.get_blocking_flow(path)
            max_flow += flow
            self.add_passage(path, flow)
            self.store_path(path, flow)

        self.apply_paths_to_network()

        return max_flow

    def store_path(self, path: list[BFSNode | BFSEdge], flow: int) -> None:
        """Store copies of a path (duplicated by flow).

        Parameters
        ----------
        path : list[BFSNode | BFSEdge]
            The path to store.
        flow : int
            Number of copies to store.
        """
        for _ in range(flow):
            self.paths.append(path.copy())

    def add_zone_state(
                self,
                zone_history: dict[int, dict[Zone, list[Drone]]],
                step: int,
                zone: Zone,
                drone: Drone
            ) -> None:
        """Record a drone's presence in a zone at a specific step.

        Parameters
        ----------
        zone_history : dict
            History dictionary to update.
        step : int
            The time step.
        zone : Zone
            The zone where the drone is.
        drone : Drone
            The drone.
        """
        zone_history.setdefault(step, {}).setdefault(zone, []).append(drone)

    def add_connection_state(
                self,
                connection_history: dict[int, dict[Connection, list[Drone]]],
                step: int,
                connection: Connection,
                drone: Drone
            ) -> None:
        """Record a drone's presence on a connection at a specific step.

        Parameters
        ----------
        connection_history : dict
            History dictionary to update.
        step : int
            The time step.
        connection : Connection
            The connection the drone is on.
        drone : Drone
            The drone.
        """
        connection_history.setdefault(step, {}).setdefault(
            connection,
            []
        ).append(drone)

    def add_idle_drone(
                self,
                zone_history: dict[int, dict[Zone, list[Drone]]],
                drone: Drone,
                last_step: int
            ) -> None:
        """Add a drone that doesn't move, keeping it at start hub.

        Parameters
        ----------
        zone_history : dict
            History dictionary to update.
        drone : Drone
            The idle drone.
        last_step : int
            The last step in the solution.
        """
        for step in range(last_step + 1):
            self.add_zone_state(
                zone_history,
                step,
                self.bfs.time_graph.network.get_start_hub(),
                drone
            )
            drone.zone_by_step[step] =\
                self.bfs.time_graph.network.get_start_hub()

    def apply_paths_to_network(self) -> None:
        """Apply found paths to the network and record trajectories."""
        network = self.bfs.time_graph.network
        zone_history: dict[int, dict[Zone, list[Drone]]] = {}
        connection_history: dict[int, dict[Connection, list[Drone]]] = {}

        for drone in network.drones:
            drone.zone_by_step.clear()
            drone.connection_by_step.clear()

        last_step: int = 0

        for index, path in enumerate(self.paths):
            if index >= len(network.drones):
                break

            drone = network.drones[index]
            current_nodes = [o for o in path if isinstance(o, BFSNode)]

            for node in current_nodes:
                real_node = node.node.real_node
                if isinstance(node.node, ConnectionNode):
                    if node.node.time > last_step:
                        last_step = node.node.time
                    continue

                if isinstance(real_node, Zone):
                    self.add_zone_state(
                        zone_history,
                        node.node.time,
                        real_node,
                        drone
                    )
                    drone.zone_by_step[node.node.time] = real_node

                if node.node.time > last_step:
                    last_step = node.node.time

            for i in range(1, len(path), 2):
                edge = path[i]

                if not isinstance(edge, BFSEdge):
                    continue

                if edge.real_connection is None:
                    continue

                if not isinstance(edge.node2.node, ConnectionNode):
                    continue

                transition_step: int = edge.node2.node.time
                self.add_connection_state(
                    connection_history,
                    transition_step,
                    edge.real_connection,
                    drone
                )
                drone.connection_by_step.update(
                        {transition_step: edge.real_connection}
                    )

                if transition_step > last_step:
                    last_step = transition_step

        for drone in network.drones[len(self.paths):]:
            self.add_idle_drone(zone_history, drone, last_step)

        if not zone_history:
            for drone in network.drones:
                start = network.get_start_hub()
                self.add_zone_state(zone_history, 0, start, drone)
                drone.zone_by_step[0] = start

        for drone in network.drones:
            arrival_steps = [
                step
                for step, zone in drone.zone_by_step.items()
                if zone is network.get_end_hub()
            ]

            if not arrival_steps:
                continue

            first_arrival: int = min(arrival_steps) + 1
            for step in range(first_arrival, last_step + 1):
                if drone.connection_by_step.get(step) is not None:
                    continue

                end = network.get_end_hub()
                self.add_zone_state(zone_history, step, end, drone)
                drone.zone_by_step[step] = end

        network.set_state_history(zone_history, connection_history)

    def add_passage(self, path: list[BFSNode | BFSEdge], flow: int) -> None:
        """Add flow units to all elements of a path.

        Parameters
        ----------
        path : list[BFSNode | BFSEdge]
            The path elements to increase passage on.
        flow : int
            Number of units to add.
        """
        for _object in path:
            _object.passage += flow

    def get_blocking_flow(self, path: list[BFSNode | BFSEdge]) -> int:
        """Get the maximum flow that can go through a path.

        Parameters
        ----------
        path : list[BFSNode | BFSEdge]
            The path to check.

        Returns
        -------
        int
            Minimum remaining capacity of all elements in the path.
        """
        return min(o.get_remaining_capacity() for o in path)
