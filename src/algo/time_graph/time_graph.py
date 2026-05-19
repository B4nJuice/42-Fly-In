"""Time-expanded graph for temporal pathfinding."""
from src.network.network import Network
from src.network.metadata.zone_metadata import ZoneType
from functools import lru_cache
from .node import Node
from .connection_node import ConnectionNode

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.network.zone.zone import Zone


class TimeGraph:
    """Time-expanded graph representation of the network.

    Expands zones and connections over time steps for pathfinding algorithms.

    Parameters
    ----------
    network : Network
        The network to expand in time.
    """
    def __init__(self, network: Network) -> None:
        """Initialize a time-expanded graph.

        Parameters
        ----------
        network : Network
            The network to expand.
        """
        self.network: Network = network
        self.nodes: list[Node] = []
        self.step: int = 0
        self.step_dict: dict[int, set[Node]] = {
            0: {self.create_node(0, self.network.get_start_hub())}
            }

    @staticmethod
    def get_real_nodes(nodes: set[Node]) -> set['Zone']:
        """Extract the real zones from a set of time-graph nodes.

        Parameters
        ----------
        nodes : set[Node]
            Time-graph nodes.

        Returns
        -------
        set[Zone]
            The set of real zones these nodes represent.
        """
        return {node.real_node for node in nodes}

    def add_connection(
                self,
                initial_node: Node,
                next_time: int,
                next_real_node: 'Zone'
            ) -> None:
        """Add a connection in the time-expanded graph.

        Parameters
        ----------
        initial_node : Node
            The source node.
        next_time : int
            The time step of the destination.
        next_real_node : Zone
            The destination zone.
        """
        new_node: Node = self.create_node(next_time, next_real_node)
        new_node.add_connection(initial_node)

    @lru_cache(maxsize=None)
    def create_node(
                self,
                time: int,
                real_node: 'Zone',
                node_type: type[Node] = Node
            ) -> Node:
        """Create or retrieve a time-graph node.

        Parameters
        ----------
        time : int
            The time step.
        real_node : Zone
            The zone.
        node_type : type[Node], optional
            The node class to instantiate (cached).

        Returns
        -------
        Node
            The created or cached node.
        """
        created_node: Node = node_type(time, real_node)
        self.nodes.append(created_node)
        return created_node

    def next_step(self) -> None:
        """Advance the time-expanded graph by one time step.

        Raises
        ------
        ConfigError
            If the end_hub becomes unreachable.
        """
        current_nodes = self.step_dict.get(self.step, set())

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
