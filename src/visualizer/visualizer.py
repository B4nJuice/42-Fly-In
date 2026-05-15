from ..network.network import Network
from ..network.zone.zone import Zone
from ..network.metadata.zone_metadata import Color
from .map import Map
from .tile import Tile

import pyray
import math
from queue import Queue
from typing import Any, cast, Callable


class Visualizer:
    def __init__(self, network: Network) -> None:
        pyray.set_trace_log_level(7)
        self.network: Network = network
        self.action_queue: Queue = Queue()
        self.frame_action_queue: Queue = Queue()
        self.background_color = pyray.BLACK
        self.tile_padding = 40
        self.step: int = 0
        self.create_map()

    @staticmethod
    def _zone_color_to_pyray(zone_color: Color) -> pyray.Color:
        color_map: dict[Color, pyray.Color] = {
            Color.NONE: pyray.BLUE,
            Color.BLUE: pyray.BLUE,
            Color.RED: pyray.RED,
            Color.GREEN: pyray.GREEN,
            Color.YELLOW: pyray.YELLOW,
            Color.GRAY: pyray.GRAY,
            Color.PURPLE: pyray.PURPLE,
            Color.BLACK: pyray.GRAY,
            Color.BROWN: pyray.BROWN,
            Color.ORANGE: pyray.ORANGE,
            Color.MAROON: pyray.MAROON,
            Color.GOLD: pyray.GOLD,
            Color.DARKRED: pyray.MAROON,
            Color.VIOLET: pyray.VIOLET,
            Color.CRIMSON: pyray.MAGENTA,
            Color.RAINBOW: pyray.RAYWHITE,
        }
        return color_map.get(zone_color, pyray.BLUE)

    @staticmethod
    def _get_zone_from_tile(tile: Tile) -> Zone | None:
        for obj in tile.objects:
            if isinstance(obj, Zone):
                return obj
        return None

    def _get_zone_center(
                self,
                zone: Zone,
                step_x: int,
                step_y: int
            ) -> tuple[int, int]:
        normalized_x, normalized_y = self.map.normalize_coords(
            zone.coords.x,
            zone.coords.y
        )
        tile = self.map.map[normalized_y][normalized_x]
        return self._get_zone_draw_position(tile, zone, step_x, step_y)

    @staticmethod
    def _get_zones_from_tile(tile: Tile) -> list[Zone]:
        return [obj for obj in tile.objects if isinstance(obj, Zone)]

    @staticmethod
    def _draw_centered_text(
                text: str,
                center_x: int,
                center_y: int,
                max_width: int,
                max_height: int,
                color: pyray.Color
            ) -> None:
        font_size = max(1, min(max_width, max_height))
        while font_size > 1 and (
                    pyray.measure_text(text, font_size) > max_width
                    or font_size > max_height
                ):
            font_size -= 1

        text_width = pyray.measure_text(text, font_size)
        text_x = center_x - (text_width // 2)
        text_y = center_y - (font_size // 2)
        pyray.draw_text(text, text_x, text_y, font_size, color)

    @staticmethod
    def _draw_right_text(
                text: str,
                padding_right: int,
                padding_bottom: int,
                color: pyray.Color,
                font_size: int = 20
            ) -> None:
        text_width = pyray.measure_text(text, font_size)
        screen_w = pyray.get_screen_width()
        screen_h = pyray.get_screen_height()
        text_x = max(0, screen_w - padding_right - text_width)
        text_y = max(0, screen_h - padding_bottom - font_size)
        pyray.draw_text(text, text_x, text_y, font_size, color)

    @staticmethod
    def _is_point_in_circle(
                point_x: int,
                point_y: int,
                center_x: int,
                center_y: int,
                radius: int
            ) -> bool:
        dx = point_x - center_x
        dy = point_y - center_y
        return (dx * dx) + (dy * dy) <= (radius * radius)

    def _get_zone_draw_position(
                self,
                tile: Tile,
                zone: Zone,
                step_x: int,
                step_y: int
            ) -> tuple[int, int]:
        zones = self._get_zones_from_tile(tile)
        center_x = self.tile_padding + tile.coords.x * step_x + (step_x // 2)
        center_y = self.tile_padding + tile.coords.y * step_y + (step_y // 2)

        if len(zones) <= 1:
            return center_x, center_y

        cols = max(1, math.ceil(math.sqrt(len(zones))))
        rows = math.ceil(len(zones) / cols)
        spacing_x = max(1, step_x // (cols + 1))
        spacing_y = max(1, step_y // (rows + 1))

        start_x = center_x - ((cols - 1) * spacing_x // 2)
        start_y = center_y - ((rows - 1) * spacing_y // 2)

        try:
            index = zones.index(zone)
        except ValueError:
            return center_x, center_y

        col = index % cols
        row = index // cols
        return start_x + col * spacing_x, start_y + row * spacing_y

    def refresh_tile(
                self,
                tile: Tile,
                step_x: int,
                step_y: int,
                radius: int,
                mouse_x: int,
                mouse_y: int
            ) -> None:
        zones = self._get_zones_from_tile(tile)
        if not zones:
            return

        if len(zones) == 1:
            color = self._zone_color_to_pyray(
                zones[0].metadata.metadata["color"]
            )
            center_x, center_y = self._get_zone_draw_position(
                tile,
                zones[0],
                step_x,
                step_y
            )
            pyray.draw_circle(center_x, center_y, radius, color)
            n_drones: int = len(zones[0].drones)
            if len(zones[0].drones) > 0:
                marker_radius = max(1, int(radius * 0.35))
                pyray.draw_circle(
                    center_x,
                    center_y,
                    marker_radius,
                    pyray.RAYWHITE
                )
            if self._is_point_in_circle(
                        mouse_x,
                        mouse_y,
                        center_x,
                        center_y,
                        radius
                    ):
                self._draw_centered_text(
                    str(n_drones),
                    center_x,
                    center_y,
                    max(2, int(radius * 1.4)),
                    max(2, int(radius * 1.4)),
                    pyray.BLACK
                )
            return

        small_radius = max(1, int(radius * 0.45))

        for zone in zones:
            x, y = self._get_zone_draw_position(tile, zone, step_x, step_y)
            color = self._zone_color_to_pyray(zone.metadata.metadata["color"])
            pyray.draw_circle(x, y, small_radius, color)
            n_drones = len(zone.drones)
            if n_drones > 0:
                marker_radius = max(1, int(small_radius * 0.5))
                pyray.draw_circle(x, y, marker_radius, pyray.RAYWHITE)
            if self._is_point_in_circle(
                        mouse_x,
                        mouse_y,
                        x,
                        y,
                        small_radius
                    ):
                self._draw_centered_text(
                    str(n_drones),
                    x,
                    y,
                    max(2, int(small_radius * 1.4)),
                    max(2, int(small_radius * 1.4)),
                    pyray.BLACK
                )

    def draw_map(self) -> None:
        self.network.apply_state_at_step(self.step)

        if not self.map.map:
            return

        map_height = len(self.map.map)
        map_width = len(self.map.map[0])

        usable_width = pyray.get_screen_width() - (self.tile_padding * 2)
        usable_height = pyray.get_screen_height() - (self.tile_padding * 2)

        step_x = max(1, usable_width // max(1, map_width))
        step_y = max(1, usable_height // max(1, map_height))
        radius = max(1, int(min(step_x, step_y) * 0.25))
        mouse_position = pyray.get_mouse_position()
        mouse_x = int(mouse_position.x)
        mouse_y = int(mouse_position.y)

        for connection in self.network.connections:
            if connection.get_zone_1() is None\
             or connection.get_zone_2() is None:
                continue

            x1, y1 = self._get_zone_center(
                    connection.get_zone_1(),
                    step_x,
                    step_y
                )
            x2, y2 = self._get_zone_center(
                    connection.get_zone_2(),
                    step_x,
                    step_y
                )
            pyray.draw_line(x1, y1, x2, y2, pyray.DARKGRAY)

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            n_drones: int = len(connection.drones)
            connection_marker_radius = max(1, int(radius * 0.55))
            if n_drones > 0:
                pyray.draw_circle(
                    center_x,
                    center_y,
                    connection_marker_radius,
                    pyray.RAYWHITE
                )
            if self._is_point_in_circle(
                        mouse_x,
                        mouse_y,
                        center_x,
                        center_y,
                        connection_marker_radius
                    ):
                self._draw_centered_text(
                    str(n_drones),
                    center_x,
                    center_y,
                    max(2, int(connection_marker_radius * 1.8)),
                    max(2, int(connection_marker_radius * 1.8)),
                    pyray.BLACK
                )

        for row in self.map.map:
            for tile in row:
                self.refresh_tile(
                        tile,
                        step_x,
                        step_y,
                        radius,
                        mouse_x,
                        mouse_y
                    )

        try:
            turn_text = f"{self.step} / {self.network.max_frames}"
            self._draw_right_text(
                    turn_text,
                    padding_right=20,
                    padding_bottom=20,
                    color=pyray.RAYWHITE,
                    font_size=20
                )
        except Exception:
            pass

    def create_map(self) -> None:
        if not self.network.zones:
            raise ValueError("No zones found in network.")

        first_zone = self.network.zones[0]
        max_x = min_x = first_zone.coords.x
        max_y = min_y = first_zone.coords.y

        for zone in self.network.zones:
            if zone.coords.x > max_x:
                max_x = zone.coords.x
            if zone.coords.x < min_x:
                min_x = zone.coords.x
            if zone.coords.y > max_y:
                max_y = zone.coords.y
            if zone.coords.y < min_y:
                min_y = zone.coords.y

        self.map: Map = Map(max_x, max_y, min_x, min_y)
        self.map.create_map()

        for zone in self.network.zones:
            x, y = self.map.normalize_coords(zone.coords.x, zone.coords.y)
            self.map.map[y][x].add_object(zone)

    def add_action_to_queue(
                self,
                function: Callable,
                args: list[Any] | None = None,
                persistent: bool = False
            ) -> None:
        if args is None:
            args = []
        if persistent:
            self.frame_action_queue.put((function, args))
            return

        self.action_queue.put((function, args))

    def call_action_from_queue(self, persistent: bool = False) -> Any:
        queue = self.frame_action_queue if persistent else self.action_queue
        function, args = queue.get()
        result = function(*args)

        if persistent:
            queue.put((function, args))

        return result

    def _execute_pending_actions(self) -> None:
        while not self.action_queue.empty():
            self.call_action_from_queue()

    def process_keys(self, key_pressed: int) -> None:
        match key_pressed:
            case 263:  # pyray.KEY_LEFT:
                self.update_step(-1)

            case 262:  # pyray.KEY_RIGHT:
                self.update_step(1)

    def update_step(self, add: int) -> None:
        self.step = min(self.network.max_frames, max(0, self.step + add))

    def start_display(self) -> None:
        pyray.init_window(1, 1, "Fly-In")

        monitor = pyray.get_current_monitor()
        width = pyray.get_monitor_width(monitor)
        height = pyray.get_monitor_height(monitor)

        pyray.set_window_size(round(width * 0.9), round(height * 0.9))
        pyray.set_window_position(round(width * 0.05), round(height * 0.05))

        pyray.set_target_fps(60)

        self.add_action_to_queue(pyray.begin_drawing, persistent=True)
        self.add_action_to_queue(
            pyray.clear_background,
            [self.background_color],
            persistent=True
        )
        self.add_action_to_queue(
            self._execute_pending_actions,
            persistent=True
        )

        infos_dict: dict[str, Any] = {"pressed_key": 0}

        self.add_action_to_queue(self.draw_map, persistent=True)
        self.add_action_to_queue(pyray.end_drawing, persistent=True)
        self.add_action_to_queue(
                lambda: infos_dict.update(
                        {"pressed_key": pyray.get_key_pressed()}
                    ),
                persistent=True
            )
        self.add_action_to_queue(
                lambda: self.process_keys(
                    cast(int, infos_dict.get("pressed_key"))
                ),
                persistent=True
                )

        while not pyray.window_should_close():
            for _ in range(self.frame_action_queue.qsize()):
                self.call_action_from_queue(persistent=True)

        pyray.close_window()
