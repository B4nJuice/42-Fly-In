from argparse import ArgumentParser

from .parser.parser import Parser
from .network.network import Network
from .network.network_object import NetworkObject
from .visualizer.visualizer import Visualizer
from .algo.time_graph.time_graph import TimeGraph
from .algo.solver.bfs.bfs import BFS
from .algo.solver.dfs.dfs import DFS
from .map_chooser.ui import ChooserUI
from .ui.logger import Logger


if __name__ == "__main__":
    arg_parser: ArgumentParser = ArgumentParser()
    arg_parser.add_argument(
        "--map-path", "-m",
        dest="map_path",
        default=None,
        help="Path to the map file to use."
    )
    arg_parser.add_argument(
        "--map-location", "-ml",
        dest="map_location",
        default="./maps",
        help="Path to the map file to use."
    )
    arg_parser.add_argument(
        "--output-file", "-o",
        dest="output_file",
        default="output.txt",
        help="File where the level summary will be written."
    )
    args = arg_parser.parse_args()

    chooser: ChooserUI = ChooserUI()

    map_path: str | None = args.map_path or chooser.start_ui(args.map_location)
    output_file: str = args.output_file

    if not map_path:
        Logger.log_warning("No path selected.")
        exit(0)

    try:
        parser = Parser(map_path)
        parser.parse_map()

        network: Network = parser.network

        network.verify()
        network.create_all_drones()

        visualizer = Visualizer(network)
        time_graph = TimeGraph(network)

        bfs = BFS(time_graph)

        dfs = DFS(bfs)

        dfs.get_all_paths()

        output_lines: list[str] = []
        for level in range(1, bfs.actual_level + 1):
            level_status: list[str] = []
            for drone in parser.network.drones:

                last_position_drone: NetworkObject | None =\
                    drone.connection_by_step.get(level - 1)
                position_drone: NetworkObject | None =\
                    drone.connection_by_step.get(level)

                if not (last_position_drone and position_drone):
                    continue

                last_position: NetworkObject = drone.zone_by_step.get(
                        level - 1, last_position_drone
                    )
                position: NetworkObject = drone.zone_by_step.get(
                        level, position_drone
                    )

                if position != last_position:
                    level_status.append(f"{drone.id}-{position.name}")
            output_lines.append(" ".join(level_status))

        try:
            with open(output_file, "w", encoding="utf-8") as output_handle:
                output_handle.write("\n".join(output_lines))
        except Exception as e:
            Logger.log_error(e)

        visualizer.start_display()

    except Exception as e:
        Logger.log_error(e)
        raise e
        exit(1)
