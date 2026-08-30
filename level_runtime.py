"""JSON-driven level and world-map runtime shared by every game stage."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class MapNode:
    key: str
    name: str
    subtitle: str
    position: tuple[int, int]
    color: tuple[int, int, int]
    default_unlocked: bool
    requires: tuple[str, ...]
    permanently_locked: bool = False


class LevelLibrary:
    def __init__(self, folder: Path):
        self.folder = Path(folder)
        map_data = self._read(self.folder / "map.json")
        self.nodes = []
        self.levels = {}
        for item in map_data.get("levels", []):
            level = self._read(self.folder / item["file"])
            if level.get("id") != item.get("id"):
                raise ValueError(f"Level id mismatch in {item['file']}")
            self.levels[item["id"]] = level
            self.nodes.append(
                MapNode(
                    item["id"],
                    item["name"],
                    item["subtitle"],
                    tuple(item["position"]),
                    tuple(item["color"]),
                    bool(item.get("default_unlocked", False)),
                    tuple(item.get("requires", [])),
                    bool(item.get("permanently_locked", False)),
                )
            )
        for item in map_data.get("hidden_levels", []):
            level = self._read(self.folder / item["file"])
            if level.get("id") != item.get("id"):
                raise ValueError(f"Level id mismatch in {item['file']}")
            self.levels[item["id"]] = level
        if not self.nodes:
            raise ValueError("levels/map.json contains no levels")

    @staticmethod
    def _read(path: Path):
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)


class LevelRuntime:
    """Holds current JSON scene state without owning rendering or input."""

    def __init__(self, library: LevelLibrary, viewport_width: int):
        self.library = library
        self.viewport_width = viewport_width
        self.level_id = None
        self.config = None
        self.scene_id = None
        self.camera_x = 0.0
        self.camera_y = 0.0
        self.triggered_waves = set()
        self.intro_time = 0.0
        self.intro_active = False
        self.intro_seen = set()

    @property
    def scene(self):
        if self.config is None or self.scene_id is None:
            return {}
        return self.config["scenes"][self.scene_id]

    @property
    def mode(self):
        return self.config.get("mode", "adventure") if self.config else "adventure"

    def start(self, level_id, players):
        self.level_id = level_id
        self.config = self.library.levels[level_id]
        self.intro_time = 0.0
        self.intro_active = bool(self.config.get("intro")) and level_id not in self.intro_seen
        self.enter_scene(self.config["start_scene"], players)

    def enter_scene(self, scene_id, players, spawn=None):
        if scene_id not in self.config.get("scenes", {}):
            raise KeyError(f"Unknown scene {scene_id!r} in {self.level_id!r}")
        self.scene_id = scene_id
        self.camera_x = 0.0
        self.camera_y = 0.0
        self.triggered_waves.clear()
        point = spawn or self.scene.get("spawn", [170, 545])
        for index, player in enumerate(players):
            player.x = float(point[0] + index * 72)
            player.y = float(point[1] + (index % 2) * 38)

    def finish_intro(self):
        if self.level_id:
            self.intro_seen.add(self.level_id)
        self.intro_active = False
        self.intro_time = 0.0

    def update_intro(self, dt):
        if not self.intro_active:
            return
        self.intro_time += dt
        if self.intro_time >= float(self.config.get("intro", {}).get("duration", 0)):
            self.finish_intro()

    def intro_caption(self):
        caption = ""
        for beat in self.config.get("intro", {}).get("beats", []):
            if self.intro_time >= float(beat.get("at", 0)):
                caption = str(beat.get("caption", ""))
        return caption

    def update_camera(self, players, dt):
        if not players or not self.scene.get("camera_follow", False):
            self.camera_x = 0.0
            return
        average_x = sum(player.x for player in players) / len(players)
        world_width = float(self.scene.get("world_width", self.viewport_width))
        target = average_x - self.viewport_width * 0.43
        target = max(0.0, min(max(0.0, world_width - self.viewport_width), target))
        self.camera_x += (target - self.camera_x) * min(1.0, dt * 5.5)

    def screen_x(self, world_x):
        return float(world_x) - self.camera_x

    def screen_y(self, world_y):
        return float(world_y) - self.camera_y

    def active_waves(self, players, completed_stories=None):
        if not players:
            return []
        completed_stories = set(completed_stories or ())
        lead_x = max(player.x for player in players)
        activated = []
        for wave in self.scene.get("waves", []):
            wave_id = wave.get("id", str(wave.get("trigger_x")))
            required_story = wave.get("after_story")
            if required_story and (self.level_id, str(required_story)) not in completed_stories:
                continue
            if wave_id not in self.triggered_waves and lead_x >= float(wave.get("trigger_x", 0)):
                self.triggered_waves.add(wave_id)
                activated.append(wave)
        return activated

    def nearby_door(self, player):
        for door in self.scene.get("doors", []):
            dx = player.x - float(door.get("x", 0))
            dy = player.y - float(door.get("y", 520))
            if dx * dx + dy * dy <= float(door.get("radius", 90)) ** 2:
                return door
        return None

    def nearby_item(self, player, collection):
        for item in self.scene.get(collection, []):
            dx = player.x - float(item.get("x", 0))
            dy = player.y - float(item.get("y", 520))
            if dx * dx + dy * dy <= 58**2:
                return item
        return None
