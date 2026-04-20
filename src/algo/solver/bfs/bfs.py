from src.algo.time_graph.time_graph import TimeGraph
from src.algo.time_graph.node import Node
from src.network.connection.connection import Connection
from .bfs_node import BFSNode
from .bfs_arette import BFSArette


class BFS:
    def __init__(self, time_graph: TimeGraph) -> None:
        self.time_graph: TimeGraph = time_graph
        self.start_node: BFSNode = self.create_bfs_node(
                list(self.time_graph.step_dict.get(0))[0],
                0
            )

        self.search_arettes(self.start_node)

    def search_arettes(self, node: BFSNode) -> None:
        for node2, connection in node.node.connections:
            new_node: BFSNode = self.create_bfs_node(node.node, node.level + 1)

            if new_node:
                arette: BFSArette = self.create_bfs_arette(
                        node,
                        new_node,
                        connection
                    )

                if arette:
                    node.arettes.append(arette)

    def create_bfs_node(self, node: Node, level: int) -> BFSNode | None:
        capacity: int = node.real_node.metadata.metadata.get("max_drones")

        if capacity <= 0:
            return

        return BFSNode(node, level, capacity)

    def create_bfs_arette(
                self,
                node1: BFSNode,
                node2: BFSNode,
                real_connection: Connection | None
            ) -> BFSArette | None:
        capacity: int = 0

        try:
            capacity = real_connection.metadata.metadata.get(
                    "max_link_capacity"
                )
        except Exception:
            capacity = node1.capacity

        if capacity <= 0:
            return

        return BFSArette(node1, node2, capacity)
