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
                visited_edges: set[BFSEdge]
            ) -> list[BFSNode | BFSEdge] | None:
        starting_node: BFSNode = path[-1]

        if starting_node.get_remaining_capacity() <= 0:
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
                            path, visited, visited_edges
                        )

                    if new_path:
                        return new_path

                    del path[path_len:]
                    visited_edges.discard(next_edge)

        visited.discard(starting_node)
        return None
