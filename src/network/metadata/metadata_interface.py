from abc import ABC, abstractmethod
from typing import Any


class MetadataInterface(ABC):
    @abstractmethod
    def __init__(self, metadata: dict[str, Any]) -> None:
        ...

    @abstractmethod
    def verify_metadata(self) -> None:
        ...
