from ..bfs.bfs import BFS
from ..bfs.bfs_node import BFSNode
from ..bfs.bfs_edge import BFSEdge
from src.algo.time_graph.connection_node import ConnectionNode
from src.network.zone.zone import Zone
from src.network.drone.drone import Drone
from src.network.connection.connection import Connection


class DFS:
    def __init__(self, bfs: BFS) -> None:
        self.bfs: BFS = bfs
        self.paths: list[list[BFSNode | BFSEdge]] = []

    def create_path(
                self,
                path: list[BFSNode | BFSEdge],
                visited: set[BFSNode],
                visited_edges: set[BFSEdge],
                dead_ends: set[BFSNode]
            ) -> list[BFSNode | BFSEdge] | None:
        starting_node: BFSNode = path[-1]

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

                    new_path: list[BFSNode | BFSEdge] = self.create_path(
                            path, visited, visited_edges, dead_ends
                        )

                    if new_path:
                        return new_path

                    del path[path_len:]
                    visited_edges.discard(next_edge)

        visited.discard(starting_node)
        dead_ends.add(starting_node)
        return None

    def get_all_paths(self) -> int:
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
        for _ in range(flow):
            self.paths.append(path.copy())

    def add_zone_state(
                self,
                zone_history: dict[int, dict[Zone, list[Drone]]],
                step: int,
                zone: Zone,
                drone: Drone
            ) -> None:
        zone_history.setdefault(step, {}).setdefault(zone, []).append(drone)

    def add_connection_state(
                self,
                connection_history: dict[int, dict[Connection, list[Drone]]],
                step: int,
                connection: Connection,
                drone: Drone
            ) -> None:
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
        for step in range(last_step + 1):
            self.add_zone_state(
                zone_history,
                step,
                self.bfs.time_graph.network.start_hub,
                drone
            )
            drone.zone_by_step[step] = self.bfs.time_graph.network.start_hub

    def apply_paths_to_network(self) -> None:
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
                self.add_zone_state(zone_history, 0, network.start_hub, drone)
                drone.zone_by_step[0] = network.start_hub

        for drone in network.drones:
            arrival_steps = [
                step
                for step, zone in drone.zone_by_step.items()
                if zone is network.end_hub
            ]

            if not arrival_steps:
                continue

            first_arrival: int = min(arrival_steps) + 1
            for step in range(first_arrival, last_step + 1):
                if drone.connection_by_step.get(step) is not None:
                    continue

                self.add_zone_state(zone_history, step, network.end_hub, drone)
                drone.zone_by_step[step] = network.end_hub

        network.set_state_history(zone_history, connection_history)

    def add_passage(self, path: list[BFSNode | BFSEdge], flow: int) -> None:
        for _object in path:
            _object.passage += flow

    def get_blocking_flow(self, path: list[BFSNode | BFSEdge]) -> int:
        return min(o.get_remaining_capacity() for o in path)
