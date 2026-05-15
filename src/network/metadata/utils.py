from typing import Any, Callable


class MetadataError(Exception):
    def __init__(self, message: str):
        super().__init__(f"Metadata Error: {message}")


class ConversionError(MetadataError):
    def __init__(self, message: str):
        super().__init__(f"Conversion Error: {message}")


class MetadataUtils:
    @staticmethod
    def transfrom_to_dict(metadata: str) -> dict[str, str]:
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
                types: dict[str, Callable]
            ) -> dict[str, Any]:

        converted_metadata: dict[str, Any] = {}

        for key, value in metadata.items():
            try:

                def identity(x: str) -> str:
                    return x

                converted_metadata.update(
                        {key: types.get(key, identity)(value)}
                    )
            except Exception as e:
                raise ConversionError(f"key: {key}, value:{value} {e}")

        return converted_metadata
