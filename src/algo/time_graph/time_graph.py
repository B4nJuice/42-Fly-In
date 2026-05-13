from src.network.network import Network
from src.network.network_object import NetworkObject
from src.network.metadata.zone_metadata import ZoneType
from functools import lru_cache
from src.parser.parser import ConfigError
from .node import Node
from .connection_node import ConnectionNode


class TimeGraph:
    def __init__(self, network: Network) -> None:
        self.network: Network = network
        self.nodes: list[Node] = []
        self.step: int = 0
        self.step_dict: dict[int, set[Node]] = {
                0: {self.create_node(0, self.network.start_hub)}
            }

    @staticmethod
    def get_real_nodes(nodes: set[Node]) -> set[NetworkObject]:
        return {node.real_node for node in nodes}

    def add_connection(
                self,
                initial_node: Node,
                next_time: int,
                next_real_node: NetworkObject
            ):
        new_node: Node = self.create_node(next_time, next_real_node)
        new_node.add_connection(initial_node)

    @lru_cache(maxsize=None)
    def create_node(
                self,
                time: int,
                real_node: NetworkObject,
                node_type: type[Node] = Node
            ) -> Node:

        created_node: Node = node_type(time, real_node)
        self.nodes.append(created_node)
        return created_node

    def next_step(self) -> None:
        current_nodes = self.step_dict.get(self.step, set())
        previous_nodes = self.step_dict.get(self.step - 1, set())
        previous_previous_nodes = self.step_dict.get(self.step - 2, set())

        if self.step > 2:
            if (
                    self.get_real_nodes(current_nodes)
                    == self.get_real_nodes(previous_nodes)
                    == self.get_real_nodes(previous_previous_nodes)
                ) and not [n for n in self.get_real_nodes(
                        current_nodes
                    ) if n.metadata.end_hub]:
                raise ConfigError("end_hub is not reachable.")

        for node in current_nodes:
            if isinstance(node, ConnectionNode):
                destination_node: Node = self.create_node(
                    self.step + 1,
                    node.real_node
                )
                node.add_connection(destination_node)
                self.step_dict.setdefault(self.step + 1, set()).add(
                    destination_node
                )
                continue

            else:
                wait_time: int = self.step + 1
                wait_node: Node = self.create_node(wait_time, node.real_node)
                node.add_connection(wait_node)
                self.step_dict.setdefault(wait_time, set()).add(wait_node)

            for zone, connection in node.real_node.get_connections():

                step_to_add: int = 1

                time: int = self.step + step_to_add

                next_node: Node = self.create_node(time, zone)
                if zone.metadata.metadata.get("zone") == ZoneType.RESTRICTED:
                    next_node = self.create_node(
                        time,
                        zone,
                        ConnectionNode
                    )

                node.add_connection(next_node, connection)
                self.step_dict.setdefault(time, set()).add(next_node)

        self.step += 1
