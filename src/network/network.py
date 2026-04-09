from .zone.zone import Zone


class Network:
    def __init__(self) -> None:
        self.nb_drones: int | None = None
        self.start_hub: Zone = None
        self.end_hub: Zone = None
        self.zones: list[Zone] = []

    def set_nb_drones(self, nb_drones: int) -> None:
        if self.nb_drones is None:
            self.nb_drones = nb_drones
        else:
            raise ValueError("nb_drones can be declared only once.")

    def set_start_hub(self, start_hub: Zone):
        if self.start_hub is None:
            self.start_hub = start_hub
        else:
            raise ValueError("start_hub can be declared only once.")

    def set_end_hub(self, end_hub: Zone):
        if self.end_hub is None:
            self.end_hub = end_hub
        else:
            raise ValueError("end_hub can be declared only once.")
