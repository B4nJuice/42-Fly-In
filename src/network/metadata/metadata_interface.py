"""Abstract interface for metadata classes."""
from abc import ABC, abstractmethod
from typing import Any


class MetadataInterface(ABC):
    """Abstract base class for metadata objects.

    Attributes
    ----------
    start_hub : bool
        Flag indicating if this metadata represents a start hub.
    end_hub : bool
        Flag indicating if this metadata represents an end hub.
    """
    start_hub: bool
    end_hub: bool

    @abstractmethod
    def __init__(self, metadata: dict[str, Any]) -> None:
        """Initialize metadata from a dictionary.

        Parameters
        ----------
        metadata : dict[str, Any]
            Dictionary containing metadata configuration.
        """
        ...

    @abstractmethod
    def verify_metadata(self) -> None:
        """Verify that metadata is valid and complete.

        Raises
        ------
        MetadataError
            If metadata is invalid or incomplete.
        """
        ...
