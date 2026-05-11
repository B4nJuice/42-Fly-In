from .map_chooser import mapChooser
from .utils.terminal import TerminalStyler

class chooserUI:

    @staticmethod
    def print_choices(dirs: list [str], files: list[str]) -> None:
        for _dir in dirs:
            print(_dir)

        for file in files:
            print(files)

    def start_ui(self) -> None:
        dirs, files = mapChooser.get_choices("maps")
        self.print_choices(dirs, files)