"""Interactive UI for selecting map files."""
from .map_chooser import MapChooser
from .utils.terminal import TerminalStyler, Colors
from src.parser.parser import Parser
import contextlib
import os
import io
from enum import Enum


class Keys(Enum):
    """Terminal key codes for navigation."""
    LEFT = "\033[D"
    RIGHT = "\033[C"
    UP = "\033[A"
    DOWN = "\033[B"
    ESC = "\033"
    ENTER = "\n"
    ENTER2 = "\r"


class ChooserUI:
    """Interactive UI for browsing and selecting map files.

    Allows navigation through directories and selection of map files
    with validation feedback.
    """
    def __init__(self) -> None:
        """Initialize the map chooser UI."""
        self._index_cache: dict[str, int] = {}
        self._current_files: list[str] = []
        self._current_path: str = ""

    def render_choice(self, choice: str, selected: bool) -> str:
        """Render a single menu choice with optional highlighting.

        Parameters
        ----------
        choice : str
            The choice text.
        selected : bool
            Whether this choice is currently selected.

        Returns
        -------
        str
            Rendered choice string with formatting.
        """
        if selected:
            return TerminalStyler.colored_text(
                    [Colors.BOLD, Colors.CYAN],
                    choice
                )

        return TerminalStyler.colored_text([], choice)

    def render_menu(
                self,
                choices: list[str],
                selected_index: int,
                clear: bool = True
            ) -> None:
        """Display the menu with validation status for each choice.

        Parameters
        ----------
        choices : list[str]
            The menu choices to display.
        selected_index : int
            Index of the currently selected choice.
        clear : bool, optional
            Whether to clear previous menu before rendering.
        """
        if clear:
            TerminalStyler.clear_x_lines(len(choices))

        for choice_index, choice in enumerate(choices):

            suffix: str = ""

            if choice in self._current_files:
                try:
                    output: io.StringIO = io.StringIO()
                    with contextlib.redirect_stdout(output):
                        parser: Parser = Parser(
                                os.path.join(self._current_path, choice)
                            )

                        parser.parse_map()
                        parser.network.verify()

                        suffix = TerminalStyler.colored_text(
                                [Colors.GREEN], " [VALID]"
                            )
                except Exception:
                    suffix = TerminalStyler.colored_text(
                            [Colors.RED], " [INVALID]"
                        )

            print(
                self.render_choice(choice, choice_index == selected_index)
                + suffix
            )

    def can_go_up(self, path: str) -> bool:
        """Check if we can navigate up from current path.

        Parameters
        ----------
        path : str
            The current path.

        Returns
        -------
        bool
            True if parent directory exists and is different.
        """
        return os.path.dirname(path) != path

    def get_choices(self, path: str) -> tuple[list[str], list[str], list[str]]:
        """Get directories, files, and combined choices from a path.

        Parameters
        ----------
        path : str
            The path to browse.

        Returns
        -------
        tuple[list[str], list[str], list[str]]
            Tuple of (directories, files, all_choices).
        """
        dirs, files = MapChooser.get_choices(path)
        choices: list[str] = []

        if self.can_go_up(path):
            choices.append("..")

        choices.extend(dirs)
        choices.extend(files)

        return dirs, files, choices

    def restore_index(self, path: str, max_index: int) -> int:
        """Restore the previously selected index for a path.

        Parameters
        ----------
        path : str
            The directory path.
        max_index : int
            Maximum valid index.

        Returns
        -------
        int
            The cached index or 0 if not cached, clamped to valid range.
        """
        if max_index < 0:
            return 0

        cached_index = self._index_cache.get(path, 0)
        return max(0, min(cached_index, max_index))

    def switch_directory(
                self,
                current_path: str,
                current_index: int,
                choices: list[str],
                next_path: str,
            ) -> tuple[str, list[str], list[str], list[str], int]:
        """Switch to a different directory.

        Parameters
        ----------
        current_path : str
            The current directory path.
        current_index : int
            The currently selected index.
        choices : list[str]
            The current menu choices.
        next_path : str
            The path to navigate to.

        Returns
        -------
        tuple[str, list[str], list[str], list[str], int]
            Tuple of (path, dirs, files, choices, selected_index).
        """
        self._index_cache[current_path] = current_index
        TerminalStyler.clear_x_lines(len(choices))

        updated_path = os.path.abspath(next_path)
        dirs, files, updated_choices = self.get_choices(updated_path)
        self._current_files = files
        self._current_path = updated_path
        updated_index = self.restore_index(
                updated_path, len(updated_choices) - 1
            )

        self.render_menu(updated_choices, updated_index, clear=False)
        return updated_path, dirs, files, updated_choices, updated_index

    def start_ui(self, base_path: str = "./maps") -> str | None:
        """Start the interactive UI for map selection.

        Parameters
        ----------
        base_path : str, optional
            The starting directory path, defaults to "./maps".

        Returns
        -------
        str | None
            The absolute path to the selected map file, or None if cancelled.
        """
        current_path = os.path.abspath(base_path)
        dirs, files, choices = self.get_choices(current_path)
        self._current_files = files
        self._current_path = current_path

        if not choices:
            return None

        index = self.restore_index(current_path, len(choices) - 1)
        self.render_menu(choices, index, clear=False)

        while True:
            pressed_key: str = TerminalStyler.get_key()
            max_index = len(choices) - 1

            match pressed_key:
                case Keys.ESC.value:
                    TerminalStyler.clear_x_lines(len(choices))
                    return None

                case Keys.DOWN.value:
                    if index < max_index:
                        index += 1
                        self.render_menu(choices, index)

                case Keys.UP.value:
                    if index > 0:
                        index -= 1
                        self.render_menu(choices, index)

                case Keys.RIGHT.value | Keys.ENTER.value | Keys.ENTER2.value:
                    selected_choice = choices[index]

                    if selected_choice == "..":
                        current_path, dirs, files, choices, index = (
                            self.switch_directory(
                                current_path,
                                index,
                                choices,
                                os.path.dirname(current_path),
                            )
                        )

                    elif selected_choice in dirs:
                        current_path, dirs, files, choices, index =\
                            self.switch_directory(
                                current_path,
                                index,
                                choices,
                                os.path.join(current_path, selected_choice),
                            )

                    else:
                        TerminalStyler.clear_x_lines(len(choices))
                        return os.path.join(current_path, selected_choice)

                case Keys.LEFT.value:
                    if self.can_go_up(current_path):
                        current_path, dirs, files, choices, index =\
                            self.switch_directory(
                                current_path,
                                index,
                                choices,
                                os.path.dirname(current_path),
                            )
