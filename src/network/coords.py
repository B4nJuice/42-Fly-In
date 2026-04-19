class Coords:
    def __init__(self, x: str | int = "0", y: str | int = "0"):
        self.x: int = int(x)
        self.y: int = int(y)
        self.raw = f"{x} {y}"
