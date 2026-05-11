import os


class mapChooser:
    @staticmethod
    def get_choices(base_path: str) -> tuple(list[str]):
        items: list[str] = os.listdir(base_path) 
        dirs: list [str] = [item for item in items if os.path.isdir(os.path.join(base_path, item))]
        files: list[str] = list(set(items) - set(dirs))

        return(dirs, files)