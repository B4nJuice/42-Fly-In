"""Main entry point for the Fly-In drone delivery simulator.

This module orchestrates the complete workflow:
1. Parse map configuration from a file
2. Build and verify the network
3. Compute optimal drone routes using BFS and DFS
4. Display results and launch visualization
"""
from argparse import ArgumentParser

from .parser.parser import Parser
from .network.network import Network
from .visualizer.visualizer import Visualizer
from .algo.time_graph.time_graph import TimeGraph
from .algo.solver.bfs.bfs import BFS
from .algo.solver.dfs.dfs import DFS
from .map_chooser.ui import ChooserUI
from .ui.logger import Logger
from typing import TYPE_CHECKING, Union, cast

if TYPE_CHECKING:
    from src.network.zone.zone import Zone
    from src.network.connection.connection import Connection


def setup_arguments() -> tuple[str | None, str]:
    """Parse and handle command-line arguments.

    Returns
    -------
    tuple[str | None, str]
        (map_path, output_file) - Selected map path and output file name
    """
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
        help="Path to the map directory to use."
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

    return map_path, args.output_file


def parse_and_verify_network(map_path: str) -> Network:
    """Parse map file and verify network integrity.

    Parameters
    ----------
    map_path : str
        Path to the map file to parse

    Returns
    -------
    Network
        Verified network with drones created
    """
    parser = Parser(map_path)
    parser.parse_map()

    network: Network = parser.network
    network.verify()
    network.create_all_drones()

    return network


def compute_drone_routes(network: Network) -> tuple[BFS, Visualizer]:
    """Compute optimal drone routes using Dinitz algorithm.

    Parameters
    ----------
    network : Network
        The network to compute routes for

    Returns
    -------
    tuple[BFS, Visualizer]
        BFS solver and visualizer for rendering
    """
    visualizer = Visualizer(network)
    time_graph = TimeGraph(network)

    bfs = BFS(time_graph)
    dfs = DFS(bfs)
    dfs.get_all_paths()

    return bfs, visualizer


def generate_output(network: Network, bfs: BFS, output_file: str) -> None:
    """Generate and write drone movement output to file.

    Parameters
    ----------
    network : Network
        The network containing drones
    bfs : BFS
        BFS solver with computed levels
    output_file : str
        Path to output file
    """
    output_lines: list[str] = []

    for level in range(1, bfs.actual_level + 1):
        level_status: list[str] = []

        for drone in network.drones:
            last_position_drone: Union['Connection', None] = \
                drone.connection_by_step.get(level - 1)
            position_drone: Union['Connection', None] = \
                drone.connection_by_step.get(level)

            if last_position_drone and position_drone:
                continue

            last_position_drone = cast('Connection', last_position_drone)
            position_drone = cast('Connection', position_drone)

            last_position: Union['Zone', 'Connection'] = \
                drone.zone_by_step.get(level - 1, last_position_drone)
            position: Union['Zone', 'Connection'] = \
                drone.zone_by_step.get(level, position_drone)

            if position != last_position:
                level_status.append(f"{drone.id}-{position.name}")

        output_lines.append(" ".join(level_status))

    with open(output_file, "w", encoding="utf-8") as output_handle:
        output_handle.write("\n".join(output_lines))


def main() -> None:
    """Main orchestration function."""
    map_path, output_file = setup_arguments()

    if not map_path:
        Logger.log_warning("No path selected.")
        return

    network = parse_and_verify_network(map_path)
    bfs, visualizer = compute_drone_routes(network)
    generate_output(network, bfs, output_file)
    visualizer.start_display()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        Logger.log_error(e)
        exit(1)
