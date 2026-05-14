from typing import Protocol
from .metadata.metadata_interface import MetadataInterface


class NetworkObject(Protocol):
    name: str
    metadata: MetadataInterface
