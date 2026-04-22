from .parser.parser import Parser
from .visualizer.visualizer import Visualizer
from .algo.time_graph.time_graph import TimeGraph
from .algo.solver.bfs.bfs import BFS
from .algo.solver.dfs.dfs import DFS


if __name__ == "__main__":
    parser = Parser("./map.txt")
    parser.parse_map()
    parser.network.verify()
    visualizer = Visualizer(parser.network)
    # visualizer.start_display()
    time_graph = TimeGraph(parser.network)

    bfs = BFS(time_graph)

    dfs = DFS(bfs)

    print(dfs.get_all_paths())
    print(bfs.actual_level)
