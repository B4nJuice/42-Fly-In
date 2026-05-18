"""Utilities for handling metadata parsing and type conversion."""
from typing import Any, Callable


class MetadataError(Exception):
    """Exception raised for metadata-related errors.

    Parameters
    ----------
    message : str
        The error message describing what went wrong.
    """
    def __init__(self, message: str):
        """Initialize MetadataError with a formatted message.

        Parameters
        ----------
        message : str
            The error message.
        """
        super().__init__(f"Metadata Error: {message}")


class ConversionError(MetadataError):
    """Exception raised when type conversion fails for metadata values.

    Parameters
    ----------
    message : str
        The error message describing the conversion failure.
    """
    def __init__(self, message: str):
        """Initialize ConversionError with a formatted message.

        Parameters
        ----------
        message : str
            The error message.
        """
        super().__init__(f"Conversion Error: {message}")


class MetadataUtils:
    """Utility class for parsing and converting metadata strings."""

    @staticmethod
    def transform_to_dict(metadata: str) -> dict[str, str]:
        """Parse metadata string into a dictionary.

        Parameters
        ----------
        metadata : str
            Metadata string in format "[key1=value1 key2=value2 ...]"

        Returns
        -------
        dict[str, str]
            Dictionary mapping keys to their string values.

        Raises
        ------
        MetadataError
            If metadata format is invalid or contains duplicate keys.
        """
        if not metadata.startswith("[") or not metadata.endswith("]"):
            raise MetadataError(
                "metadata has to start with '[' and end with ']'."
            )
        metadata = metadata[1:-1]

        datas: list[str] = metadata.split()

        metadata_dict: dict[str, str] = {}

        for data in datas:
            try:
                key, value = data.split("=", maxsplit=1)
            except Exception:
                raise MetadataError(
                        f"Missing value for key: {data.replace('=', '')}"
                    )
            if key in metadata_dict.keys():
                raise MetadataError(f"duplicate key in metadata: {key}.")
            metadata_dict.update({key: value})

        return metadata_dict

    @staticmethod
    def convert_metadata_types(
                metadata: dict[str, str],
                types: dict[str, Callable[[str], Any]]
            ) -> dict[str, Any]:
        """Convert metadata values to their specified types.

        Parameters
        ----------
        metadata : dict[str, str]
            Dictionary with string keys and values to convert.
        types : dict[str, Callable[[str], Any]]
            Mapping of keys to conversion functions. Missing defaults to id.

        Returns
        -------
        dict[str, Any]
            Dictionary with converted values per type mappings.

        Raises
        ------
        ConversionError
            If type conversion fails for any key-value pair.
        """
        converted_metadata: dict[str, Any] = {}

        for key, value in metadata.items():

            def first_param(x: str) -> str:
                return x

            try:
                converted_metadata.update(
                        {key: types.get(key, first_param)(value)}
                    )
            except Exception as e:
                raise ConversionError(f"key: {key}, value:{value} {e}")

        return converted_metadata
