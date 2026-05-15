"""Protocol defining the interface for network objects."""
from typing import Protocol
from .metadata.metadata_interface import MetadataInterface


class NetworkObject(Protocol):
    """Protocol for objects in the network (zones and connections).

    Attributes
    ----------
    name : str
        The name identifier of the network object.
    metadata : MetadataInterface
        Metadata associated with the object.
    """
    name: str
    metadata: MetadataInterface
