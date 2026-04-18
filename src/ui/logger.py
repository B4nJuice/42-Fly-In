from .terminal_styler import TerminalStyler, Colors


class Logger:
    @staticmethod
    def log_warning(message: str) -> None:
        print(
                TerminalStyler.colored_text(
                    [Colors.BOLD, Colors.YELLOW], "[WARNING]"
                ),
                TerminalStyler.colored_text([Colors.YELLOW], message)
            )
