from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..connection.connection import Connection
    from ..zone.zone import Zone


class Drone():
    def __init__(self, id: str) -> None:
        self.id: str = id
        self.zone_by_step: dict[int, 'Zone'] = {}
        self.connection_by_step: dict[int, 'Connection'] = {}
