from . metadata_interface import MetadataInterface
from .utils import MetadataUtils, MetadataError
from typing import Any


class ConnectionMetadata(MetadataInterface):
    def __init__(self, metadata: dict[str, Any]) -> None:
        self.default_metadata: dict[str, Any] = {
            "max_link_capacity": 1,
        }

        self.types: dict[str, callable] = {
            "max_link_capacity": int,
        }

        converted_metadata: dict[str, Any] = {}
        converted_metadata = MetadataUtils.convert_metadata_types(
            MetadataUtils.transfrom_to_dict(metadata),
            self.types
        )

        self.metadata: dict[str, Any] = {}
        self.metadata.update(self.default_metadata)
        self.metadata.update(converted_metadata)

    def verify_metadata(self) -> None:
        if diff := (self.metadata.keys() - self.default_metadata.keys()):
            raise MetadataError(f"Invalid metadata fields : {diff}")
