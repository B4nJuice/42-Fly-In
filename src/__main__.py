from .parser.parser import Parser
from .visualizer.visualizer import Visualizer
from .algo.time_graph.time_graph import TimeGraph
from .algo.solver.bfs.bfs import BFS
from .algo.solver.dfs.dfs import DFS
from .map_chooser.ui import chooserUI
from .ui.logger import Logger


if __name__ == "__main__":
    chooser: chooserUI = chooserUI()

    map_path: str | None = chooser.start_ui()

    if not map_path:
        Logger.log_warning("No path selected.")
        exit(0)

    try:
        parser = Parser(map_path)
        parser.parse_map()
        parser.network.verify()
        parser.network.create_all_drones()

        visualizer = Visualizer(parser.network)
        time_graph = TimeGraph(parser.network)

        bfs = BFS(time_graph)

        dfs = DFS(bfs)

        dfs.get_all_paths()
        bfs.actual_level
        visualizer.start_display()
    except Exception as e:
        Logger.log_error(e)
        exit(1)
