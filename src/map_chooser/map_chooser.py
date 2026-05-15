"""Map selection utilities for discovering test scenarios."""
import os


class MapChooser:
    """Utility class for browsing map directories."""

    @staticmethod
    def get_choices(base_path: str) -> tuple[list[str], list[str]]:
        """Get subdirectories and files in a path.

        Parameters
        ----------
        base_path : str
            The path to browse.

        Returns
        -------
        tuple[list[str], list[str]]
            A tuple of (directories, files), both sorted. Returns empty lists
            if the path cannot be accessed.
        """
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
