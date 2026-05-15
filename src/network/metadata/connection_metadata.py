"""Connection metadata handling and validation."""
from . metadata_interface import MetadataInterface
from .utils import MetadataUtils, MetadataError
from typing import Any, Callable, cast


class ConnectionMetadata(MetadataInterface):
    """Metadata for network connections.

    Parameters
    ----------
    metadata : str
        Metadata string in format "[key1=value1 key2=value2 ...]".
    """
    def __init__(self, metadata: str) -> None:
        """Initialize connection metadata.

        Parameters
        ----------
        metadata : str
            Metadata string containing connection configuration.
        """
        self.default_metadata: dict[str, Any] = {
            "max_link_capacity": 1,
        }

        self.types: dict[str, Callable[[str], Any]] = {
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
        """Verify that connection metadata is valid.

        Raises
        ------
        MetadataError
            If metadata contains invalid fields or values.
        """
        if diff := (self.metadata.keys() - self.default_metadata.keys()):
            raise MetadataError(f"Invalid metadata fields : {diff}")

        if cast(int, self.metadata.get("max_link_capacity")) <= 0:
            raise MetadataError(
                    "max_link_capacity field has to be a positive integer."
                )
