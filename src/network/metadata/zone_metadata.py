from typing import Any
from .utils import MetadataUtils


class ZoneMetadata:
    def __init__(self, metadata: dict[str, Any]) -> None:
        self.default_metadata: dict[str, Any] = {
            "zone": "normal",
            "color": None,
            "max_drones": 1,
            "start_hub": False,
            "end_hub": False,
        }

        self.types: dict[str, callable] = {
            "zone": str,
            "color": str,
            "max_drones": int,
        }

        converted_metadata: dict[str, Any] = {}
        converted_metadata = MetadataUtils.convert_metadata_types(metadata)

        self.metadata: dict[str, Any] = {}
        self.default_metadata.update(converted_metadata)

    def verify_metadata(self) -> None:
        if diff := (self.default_metadata.keys() - self.metadata.keys()):
            raise ValueError(f"Invalid metadata fields : {diff}")
