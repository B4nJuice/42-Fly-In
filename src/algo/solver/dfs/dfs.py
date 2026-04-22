from ..bfs.bfs import BFS
from ..bfs.bfs_node import BFSNode
from ..bfs.bfs_edge import BFSEdge


class DFS:
    def __init__(self, bfs: BFS) -> None:
        self.bfs: BFS = bfs

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

        for edge in starting_node.edges:
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

            print([
                o.node.real_node.name for o in path if isinstance(o, BFSNode)
            ])

            flow: int = self.get_blocking_flow(path)
            max_flow += flow
            print(flow)
            self.add_passage(path, flow)

        return max_flow

    def add_passage(self, path: list[BFSNode | BFSEdge], flow: int) -> None:
        for _object in path:
            _object.passage += flow

    def get_blocking_flow(self, path: list[BFSNode | BFSEdge]) -> int:
        return min(o.get_remaining_capacity() for o in path)
