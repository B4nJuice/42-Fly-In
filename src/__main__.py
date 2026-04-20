from .parser.parser import Parser
from .visualizer.visualizer import Visualizer
from .algo.time_graph.time_graph import TimeGraph


if __name__ == "__main__":
    parser = Parser("./map.txt")
    parser.parse_map()
    parser.network.verify()
    visualizer = Visualizer(parser.network)
    # visualizer.start_display()
    time_graph = TimeGraph(parser.network)

    for _ in range(60):
        time_graph.next_step()

    print("OK")
