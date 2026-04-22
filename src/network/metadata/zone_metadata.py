from typing import Any
from .utils import MetadataUtils, MetadataError
from .metadata_interface import MetadataInterface
from enum import Enum
from src.ui.logger import Logger


class ZoneType(Enum):
    NORMAL = "normal"
    RESTRICTED = "restricted"
    PRIORITY = "priority"
    BLOCKED = "blocked"


class Color(Enum):
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
    def __init__(self, metadata: str) -> None:
        self.default_metadata: dict[str, Any] = {
            "zone": ZoneType.NORMAL,
            "color": Color.NONE,
            "max_drones": 1,
        }

        self.types: dict[str, callable] = {
            "zone": ZoneType,
            "color": self.get_color,
            "max_drones": int,
        }

        converted_metadata: dict[str, Any] = {}
        converted_metadata = MetadataUtils.convert_metadata_types(
            MetadataUtils.transfrom_to_dict(metadata),
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
        try:
            return Color(color)
        except Exception:
            Logger.log_warning(
                    f"'{color}' color is undefined, switched to default color."
                )
            return Color.NONE

    def verify_metadata(self) -> None:
        if diff := (self.metadata.keys() - self.default_metadata.keys()):
            raise MetadataError(f"Invalid metadata fields : {diff}")

        if self.metadata.get("max_drones") <= 0:
            raise MetadataError(
                    "max_drones field has to be a positive integer."
                )

    def set_start_hub(self) -> None:
        if self.end_hub:
            raise MetadataError("a zone cannot be start_hub and end_hub")
        self.start_hub = True

    def set_end_hub(self) -> None:
        if self.end_hub:
            raise MetadataError("a zone cannot be end_hub and end_hub")
        self.end_hub = True
