from typing import Any
from .utils import MetadataUtils, MetadataError


class ZoneMetadata:
    def __init__(self, metadata: str) -> None:
        self.default_metadata: dict[str, Any] = {
            "zone": "normal",
            "color": None,
            "max_drones": 1,
        }

        self.types: dict[str, callable] = {
            "zone": str,
            "color": str,
            "max_drones": int,
        }

        converted_metadata: dict[str, Any] = {}
        converted_metadata = MetadataUtils.convert_metadata_types(
            MetadataUtils.transfrom_to_dict(metadata),
            self.types
        )

        self.metadata: dict[str, Any] = {}
        self.default_metadata.update(converted_metadata)

        self.start_hub: bool = False
        self.end_hub: bool = False

    def verify_metadata(self) -> None:
        if diff := (self.default_metadata.keys() - self.metadata.keys()):
            raise ValueError(f"Invalid metadata fields : {diff}")

    def set_start_hub(self) -> None:
        if self.end_hub:
            raise MetadataError("a zone cannot be start_hub and end_hub")
        self.start_hub = True

    def set_end_hub(self) -> None:
        if self.end_hub:
            raise MetadataError("a zone cannot be end_hub and end_hub")
        self.start_hub = True
