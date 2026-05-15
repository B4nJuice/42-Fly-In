"""Logging utilities for displaying formatted messages in the terminal."""
from .terminal_styler import TerminalStyler, Colors


class Logger:
    """Provides static methods for logging warning and error messages."""

    @staticmethod
    def log_warning(message: str) -> None:
        """Log a warning message with yellow styling.

        Parameters
        ----------
        message : str
            The warning message to display.
        """
        print(
                TerminalStyler.colored_text(
                    [Colors.BOLD, Colors.YELLOW], "[WARNING]"
                ),
                TerminalStyler.colored_text([Colors.YELLOW], message)
            )

    @staticmethod
    def log_error(error: Exception) -> None:
        """Log an error message with red styling.

        Parameters
        ----------
        error : Exception
            The exception to display as an error message.
        """
        print(
                TerminalStyler.colored_text(
                    [Colors.BOLD, Colors.RED], "[ERROR]"
                ),
                TerminalStyler.colored_text([Colors.RED], str(error))
            )
