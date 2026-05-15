from enum import Enum
import tty
import sys
import termios
import fcntl
import os


class Colors(Enum):
    """ANSI color/style escape sequences used for terminal rendering."""

    BOLD = "\033[1m"
    RESET = "\033[0m"
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"
    RED = "\033[31m"


class TerminalStyler():
    """Provide terminal styling helpers for line control and colors."""

    @staticmethod
    def clear_current_line() -> None:
        """Clear the current terminal line and move cursor to line start.

        Returns
        -------
        None
            Writes ANSI control sequences to stdout.
        """
        print("\x1b[2K\x1b[G", end="", flush=True)

    @staticmethod
    def redraw_line_at_x(line: str, x: int) -> None:
        """Redraw a line at a specific vertical position.

        Parameters
        ----------
        line : str
            The line to draw.
        x : int
            The vertical offset.
        """
        print(f"\x1b[{x}A", end="", flush=True)
        TerminalStyler.clear_current_line()
        print(line)
        print(f"\x1b[{x}B", end="", flush=True)

    @staticmethod
    def clear_x_lines(x: int) -> None:
        """Clear X lines above the current cursor position.

        Parameters
        ----------
        x : int
            Number of lines to clear.
        """
        for i in range(x):
            print("\x1b[1A", end="", flush=True)
            TerminalStyler.clear_current_line()

    @staticmethod
    def colored_text(colors: list[Colors], text: str) -> str:
        """Wrap text with ANSI color/style sequences.

        Parameters
        ----------
        colors : list[Colors]
            Ordered list of styles to apply.
        text : str
            Text to format.

        Returns
        -------
        str
            Styled text including a trailing reset sequence.
        """
        rendered_text: str = "".join([color.value for color in colors])
        rendered_text += text
        rendered_text += Colors.RESET.value
        return rendered_text

    @staticmethod
    def get_key() -> str:
        """Read a single key press from stdin, including escape sequences.

        Returns
        -------
        str
            The key pressed, including multi-character escape sequences for
            arrow keys and other special keys.
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        old_flags = fcntl.fcntl(fd, fcntl.F_GETFL)

        try:
            tty.setraw(fd)

            char = sys.stdin.read(1)

            if char == "\x1b":
                fcntl.fcntl(fd, fcntl.F_SETFL, old_flags | os.O_NONBLOCK)

                try:
                    char += sys.stdin.read(2)
                except Exception:
                    pass

            return char

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            fcntl.fcntl(fd, fcntl.F_SETFL, old_flags)
