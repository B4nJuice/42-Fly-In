from typing import Any


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
            key, value = data.split("=")
            if key in metadata_dict.keys():
                raise MetadataError(f"duplicate key in metadata: {key}.")
            metadata_dict.update({key, value})

        return metadata_dict

    @staticmethod
    def convert_metadata_types(
                metadata: dict[str, str],
                types: dict[str, callable]
            ) -> dict[str, Any]:

        converted_metadata: dict[str, Any] = {}

        for key, value in metadata.items():
            try:
                converted_metadata.update(
                        {key: types.get(key, lambda x: x)}(value)
                    )
            except Exception as e:
                raise ConversionError(f"key: {key}, value:{value} {e}")

        return converted_metadata
