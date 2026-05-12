from .parser.parser import Parser
from .visualizer.visualizer import Visualizer
from .algo.time_graph.time_graph import TimeGraph
from .algo.solver.bfs.bfs import BFS
from .algo.solver.dfs.dfs import DFS
from .map_chooser.ui import chooserUI


if __name__ == "__main__":
    chooser = chooserUI()

    map_path: str = chooser.start_ui()

    parser = Parser(map_path)
    parser.parse_map()
    parser.network.verify()

    parser.network.create_all_drones()

    print(parser.network.nb_drones)
    print(len(parser.network.drones))

    visualizer = Visualizer(parser.network)
    time_graph = TimeGraph(parser.network)

    bfs = BFS(time_graph)

    dfs = DFS(bfs)

    print(dfs.get_all_paths())
    print(bfs.actual_level)
    visualizer.start_display()

    # TODO: Erase prints