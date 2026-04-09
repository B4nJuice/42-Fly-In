from ..coords import Coords
from ..metadata import zone_metadata


class Zone:
    def __init__(
                self,
                name: str,
                coords: Coords,
                metadata: zone_metadata
            ):
        self.name: str = name
        self.metadata: zone_metadata = metadata
