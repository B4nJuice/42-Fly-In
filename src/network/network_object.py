from abc import ABC
from .metadata.metadata_interface import MetadataInterface


class NetworkObject(ABC):
    @property
    def name(self) -> str:
        pass

    @property
    def metadata(self) -> MetadataInterface:
        pass
