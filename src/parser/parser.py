class Parser:
    def __init__(self, file_path: str) -> None:
        self.file_path: str = file_path
        self.lines: list[str] = self.clean_lines()

    @staticmethod
    def erase_comment(line: str):
        return line.split("#")[0].strip()

    def clean_lines(self) -> None:
        lines: list[str] = []
        clean_lines: list[str] = []

        with open(self.file_path, "r") as opened_file:
            lines = opened_file.readlines()

        clean_lines: list[str] = [
            clean_line
            for line in lines if (clean_line := self.erase_comment(line))
        ]

        return clean_lines


if __name__ == "__main__":
    parser = Parser("./map.txt")
    print("\n".join(parser.lines))
