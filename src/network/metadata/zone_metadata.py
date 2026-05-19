"""Zone metadata handling, types, and validation."""
from .utils import MetadataUtils, MetadataError
from .metadata_interface import MetadataInterface
from src.ui.logger import Logger

from enum import Enum
from typing import Any, Callable, cast


class ZoneType(Enum):
    """Types of zones in the network."""
    NORMAL = "normal"
    RESTRICTED = "restricted"
    PRIORITY = "priority"
    BLOCKED = "blocked"


class Color(Enum):
    """Available colors for zone visualization."""
    NONE = None
    BLUE = "blue"
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    GRAY = "gray"
    PURPLE = "purple"
    BLACK = "black"
    BROWN = "brown"
    ORANGE = "orange"
    MAROON = "maroon"
    GOLD = "gold"
    DARKRED = "darkred"
    VIOLET = "violet"
    CRIMSON = "crimson"
    RAINBOW = "rainbow"


class ZoneMetadata(MetadataInterface):
    """Metadata for network zones.

    Parameters
    ----------
    metadata : str
        Metadata string in format "[key1=value1 key2=value2 ...]".
    """
    def __init__(self, metadata: str) -> None:
        """Initialize zone metadata.

        Parameters
        ----------
        metadata : str
            Metadata string containing zone configuration.
        """
        self.default_metadata: dict[str, Any] = {
            "zone": ZoneType.NORMAL,
            "color": Color.NONE,
            "max_drones": 1,
        }

        self.types: dict[str, Callable[[str], Any]] = {
            "zone": ZoneType,
            "color": self.get_color,
            "max_drones": int,
        }

        converted_metadata: dict[str, Any] = {}
        converted_metadata = MetadataUtils.convert_metadata_types(
            MetadataUtils.transform_to_dict(metadata),
            self.types
        )

        self.metadata: dict[str, Any] = {}
        self.metadata.update(self.default_metadata)
        self.metadata.update(converted_metadata)

        if self.metadata.get("zone") == ZoneType.BLOCKED:
            self.metadata.update({"max_drones": 0})

        self.start_hub: bool = False
        self.end_hub: bool = False

    @staticmethod
    def get_color(color: str) -> Color:
        """Convert color string to Color enum.

        Parameters
        ----------
        color : str
            The color name as a string.

        Returns
        -------
        Color
            The corresponding Color enum value, or Color.NONE if invalid.
        """
        try:
            return Color(color)
        except Exception:
            Logger.log_warning(
                    f"'{color}' color is undefined, switched to default color."
                )
            return Color.NONE

    def verify_metadata(self) -> None:
        """Verify that zone metadata is valid.

        Raises
        ------
        MetadataError
            If metadata contains invalid fields or values.
        """
        if diff := (self.metadata.keys() - self.default_metadata.keys()):
            raise MetadataError(f"Invalid metadata fields : {diff}")

        if cast(int, self.metadata.get("max_drones")) <= 0 and not\
            cast(ZoneType, self.metadata.get("zone")) == ZoneType.BLOCKED:
            raise MetadataError(
                    "max_drones field has to be a positive integer."
                )

    def set_start_hub(self) -> None:
        """Mark this zone as the start hub.

        Raises
        ------
        MetadataError
            If the zone is already marked as an end hub.
        """
        if self.end_hub:
            raise MetadataError("a zone cannot be start_hub and end_hub")
        self.start_hub = True

    def set_end_hub(self) -> None:
        """Mark this zone as the end hub.

        Raises
        ------
        MetadataError
            If the zone is already marked as an end hub (sic).
        """
        if self.end_hub:
            raise MetadataError("a zone cannot be end_hub and end_hub")
        self.end_hub = True
