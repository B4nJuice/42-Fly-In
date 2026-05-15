class Coords:
    """Represents 2D coordinates for zones in the network.

    Parameters
    ----------
    x : str | int, optional
        The X coordinate, defaults to "0".
    y : str | int, optional
        The Y coordinate, defaults to "0".
    """
    def __init__(self, x: str | int = "0", y: str | int = "0"):
        """Initialize coordinates.

        Parameters
        ----------
        x : str | int, optional
            The X coordinate, defaults to "0".
        y : str | int, optional
            The Y coordinate, defaults to "0".
        """
        self.x: int = int(x)
        self.y: int = int(y)
        self.raw = f"{x} {y}"
