from src.algo.time_graph.time_graph import TimeGraph
from src.algo.time_graph.node import Node
from src.network.connection.connection import Connection
from functools import lru_cache
from .bfs_node import BFSNode
from .bfs_edge import BFSEdge


class BFS:
    def __init__(self, time_graph: TimeGraph) -> None:
        self.time_graph: TimeGraph = time_graph
        self.start_node: BFSNode = self.create_bfs_node(
                list(self.time_graph.step_dict.get(0))[0],
                0
            )

        self.search_edges(self.start_node)
        self.bfs_level: dict[int, set[BFSNode]] = {0: set([self.start_node])}
        self.actual_level: int = 0

        self.end_reached: bool = (
                self.start_node.node.real_node.metadata.end_hub
            )

    def next_level(self) -> None:
        current_level_nodes = list(self.bfs_level.get(self.actual_level, []))
        if not current_level_nodes:
            return

        for node in current_level_nodes:
            if not self.end_reached:
                if node.node.real_node.metadata.end_hub:
                    self.end_reached = True
            # print(self.actual_level,node.node.real_node.name, node.node.time)
            for n in node.get_connected_nodes():
                self.bfs_level.setdefault(self.actual_level + 1, set()).add(n)

        # print("\n--------------------\n")

        self.actual_level += 1

        for node in self.bfs_level.get(self.actual_level, []):
            self.search_edges(node)

    def search_edges(self, node: BFSNode) -> None:
        for node2, connection in node.node.connections:
            if node2.time <= node.node.time:
                continue
            new_node: BFSNode = self.create_bfs_node(node2, node.level + 1)

            if new_node:
                if any(edge.node2 == new_node for edge in node.edges):
                    continue

                edge: BFSEdge = self.create_bfs_edge(
                        node,
                        new_node,
                        connection
                    )

                if edge:
                    node.edges.append(edge)

    def grow_with_time_step(self) -> None:
        self.time_graph.next_step()

        max_known_level: int = max(self.bfs_level.keys(), default=0)

        for level in range(max_known_level + 1):
            for node in self.bfs_level.get(level, set()):
                self.search_edges(node)

        if not self.bfs_level.get(self.actual_level, set()):
            for level in range(self.actual_level - 1, -1, -1):
                if self.bfs_level.get(level, set()):
                    self.actual_level = level
                    break

        self.next_level()

    @lru_cache(maxsize=None)
    def create_bfs_node(self, node: Node, level: int) -> BFSNode | None:
        capacity: int = node.real_node.metadata.metadata.get("max_drones")

        if capacity <= 0:
            return

        return BFSNode(node, level, capacity)

    def create_bfs_edge(
                self,
                node1: BFSNode,
                node2: BFSNode,
                real_connection: Connection | None
            ) -> BFSEdge | None:
        capacity: int = 0

        try:
            capacity = real_connection.metadata.metadata.get(
                    "max_link_capacity"
                )
        except Exception:
            capacity = node1.capacity

        if capacity <= 0:
            return

        return BFSEdge(node1, node2, capacity)
