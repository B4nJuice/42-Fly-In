from .parser.parser import Parser
from .visualizer.visualizer import Visualizer


if __name__ == "__main__":
    parser = Parser("./map.txt")
    parser.parse_map()
    parser.network.verify()
    visualizer = Visualizer(parser.network)
    visualizer.start_display()
    print("OK")
