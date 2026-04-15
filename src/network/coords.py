class Coords:
    def __init__(self, x: str = "0", y: str = "0"):
        self.x = int(x)
        self.y = int(y)
        if self.x < 0 or self.y < 0:
            raise ValueError("coordinates have to be non-negative integers")
        self.raw = f"{x} {y}"
