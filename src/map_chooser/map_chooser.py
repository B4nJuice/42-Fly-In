import os


class MapChooser:
    @staticmethod
    def get_choices(base_path: str) -> tuple[list[str], list[str]]:
        try:

            items: list[str] = sorted(os.listdir(base_path))
            dirs: list[str] = [
                item for item in items if os.path.isdir(os.path.join(
                        base_path, item
                    ))
            ]
            files: list[str] = [item for item in items if item not in dirs]
        except Exception:
            return ([], [])

        return (dirs, files)
