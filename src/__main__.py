from .parser.parser import Parser
from .visualizer.visualizer import Visualizer
from .algo.time_graph.time_graph import TimeGraph
from .algo.solver.bfs.bfs import BFS
from .algo.solver.dfs.dfs import DFS
from .algo.solver.bfs.bfs_node import BFSNode


if __name__ == "__main__":
    parser = Parser("./map.txt")
    parser.parse_map()
    parser.network.verify()
    visualizer = Visualizer(parser.network)
    # visualizer.start_display()
    time_graph = TimeGraph(parser.network)

    max_time_steps: int = 120
    for _ in range(max_time_steps):
        time_graph.next_step()

    bfs = BFS(time_graph)

    max_bfs_levels: int = 120
    for _ in range(max_bfs_levels):
        if bfs.end_reached:
            break
        bfs.next_level()

    dfs = DFS(bfs)

    path = dfs.create_path([bfs.start_node], set(), set())

    try:
        print(len(path))

        print([r.node.real_node.name for r in [n for n in path if isinstance(n, BFSNode)]])
    except Exception:
        print("KO")
    else:
        print("OK")
