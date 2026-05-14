from abc import ABC, abstractmethod
from typing import Any


class MetadataInterface(ABC):
    start_hub: bool
    end_hub: bool

    @abstractmethod
    def __init__(self, metadata: dict[str, Any]) -> None:
        ...

    @abstractmethod
    def verify_metadata(self) -> None:
        ...
