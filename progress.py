"""Per-profile, per-character progression saves for the local campaign."""

from __future__ import annotations

import json
import os
import re
import threading
import time
from copy import deepcopy
from pathlib import Path


SAVE_VERSION = 3
GLOBAL_SAVE_VERSION = 3
LEGACY_CHARACTERS = {"electric": "ember", "ice": "tide", "fire": "storm", "green": "grove"}
ITEM_LIMITS = {"health_potion": 5, "bomb": 9, "horn": 1}
DEFAULT_GLOBAL_SAVE = {
    "version": GLOBAL_SAVE_VERSION,
    "unlocked_characters": ["electric", "ice", "fire", "green"],
    "unlocked_weapons": ["rusty_sword"],
    "wizard_portals": ["painter"],
    "settings": {"music_volume": 0.75, "sfx_volume": 0.75},
}
DEFAULT_SAVE = {
    "version": SAVE_VERSION,
    "equipped_weapon": None,
    "equipped_pet": None,
    "unlocked_pets": [],
    "unlocked_levels": ["home_castle"],
    "completed_levels": [],
    "stats": {"knockouts": 0, "deaths": 0},
    "level": 1,
    "xp": 0,
    "stat_points": 0,
    "attributes": {"strength": 0, "defense": 0, "magic": 0, "agility": 0},
    "gold": 25,
    "items": {"health_potion": 0, "bow": 1, "sandwich": 0, "bomb": 0, "horn": 0},
    "selected_item": "bow",
    "health": None,
    "last_checkpoint": "world_map",
    "autosave_count": 0,
}


def _safe_name(value: object, fallback: str) -> str:
    name = re.sub(r"[^A-Za-z0-9_.-]+", "_", str(value or "").strip())
    return name.strip("._") or fallback


class SaveStore:
    """Loads one JSON file for each playable character.

    Saves are also scoped to the signed-in SDBox profile so two console users
    never overwrite one another's character progression.
    """

    def __init__(self, root: Path):
        username = _safe_name(os.environ.get("SDBOX_USERNAME"), "default_user")
        self.root = Path(root) / username
        if os.environ.get("SDBOX_USER_APPDATA_DIR", None):
            self.root = Path(os.path.join(os.environ.get("SDBOX_USER_APPDATA_DIR", ""), os.path.basename(os.path.dirname(__file__))))
        self.root.mkdir(parents=True, exist_ok=True)
        self.cache: dict[str, dict] = {}
        self.pending_saves: set[str] = set()
        self.global_dirty = False
        self.next_flush_at = 0.0
        self.write_counter = 0
        self.write_lock = threading.RLock()
        self.last_save_error: OSError | None = None
        self.global_cache = self._load_global()

    @property
    def global_path(self) -> Path:
        return self.root / "global.json"

    def _load_global(self) -> dict:
        """Load profile-wide unlocks and migrate the old character-local lists once."""
        data = deepcopy(DEFAULT_GLOBAL_SAVE)
        path = self.global_path
        loaded = None
        try:
            candidate = json.loads(path.read_text(encoding="utf-8"))
            loaded = candidate if isinstance(candidate, dict) else None
        except (OSError, ValueError, TypeError):
            pass
        if loaded:
            for key in data:
                if key in loaded:
                    data[key] = loaded[key]

        should_migrate = loaded is None or int(loaded.get("version", 0)) < GLOBAL_SAVE_VERSION
        if should_migrate:
            legacy_to_current = {legacy: current for current, legacy in LEGACY_CHARACTERS.items()}
            for character_path in self.root.glob("*.json"):
                if character_path.name.lower() == "global.json":
                    continue
                try:
                    old_data = json.loads(character_path.read_text(encoding="utf-8"))
                except (OSError, ValueError, TypeError):
                    continue
                if not isinstance(old_data, dict):
                    continue
                character = str(old_data.get("character", character_path.stem))
                character = legacy_to_current.get(character, character)
                data["unlocked_characters"].append(character)
                data["unlocked_weapons"].extend(str(item) for item in old_data.get("unlocked_weapons", []))

        for key in ("unlocked_characters", "unlocked_weapons", "wizard_portals"):
            data[key] = list(dict.fromkeys(str(item) for item in data.get(key, [])))
        for character in DEFAULT_GLOBAL_SAVE["unlocked_characters"]:
            if character not in data["unlocked_characters"]:
                data["unlocked_characters"].append(character)
        if "rusty_sword" not in data["unlocked_weapons"]:
            data["unlocked_weapons"].insert(0, "rusty_sword")
        if "painter" not in data["wizard_portals"]:
            data["wizard_portals"].insert(0, "painter")
        loaded_settings = data.get("settings", {})
        if not isinstance(loaded_settings, dict):
            loaded_settings = {}
        normalized_settings = {}
        for key, default in DEFAULT_GLOBAL_SAVE["settings"].items():
            try:
                value = float(loaded_settings.get(key, default))
            except (TypeError, ValueError):
                value = float(default)
            normalized_settings[key] = max(0.0, min(1.0, value))
        data["settings"] = normalized_settings
        data["version"] = GLOBAL_SAVE_VERSION
        self.global_cache = data
        self.save_global()
        return data

    def _atomic_write(self, path: Path, data: dict) -> bool:
        """Replace a JSON save without crashing when Windows briefly locks it."""
        with self.write_lock:
            return self._atomic_write_locked(path, data)

    def _atomic_write_locked(self, path: Path, data: dict) -> bool:
        payload = json.dumps(data, indent=2, sort_keys=True) + "\n"
        self.write_counter += 1
        temporary = path.with_name(
            f".{path.name}.tmp.{os.getpid()}.{threading.get_ident()}.{self.write_counter}"
        )
        delays = (0.0, 0.005, 0.015, 0.03)
        wrote_temporary = False
        try:
            for delay in delays:
                if delay:
                    time.sleep(delay)
                try:
                    if not wrote_temporary:
                        temporary.write_text(payload, encoding="utf-8")
                        wrote_temporary = True
                    temporary.replace(path)
                    self.last_save_error = None
                    return True
                except PermissionError as exc:
                    self.last_save_error = exc
                    continue
                except OSError as exc:
                    self.last_save_error = exc
                    return False
            return False
        finally:
            try:
                if temporary.exists():
                    temporary.unlink()
            except OSError:
                pass

    def save_global(self) -> bool:
        data = getattr(self, "global_cache", None)
        if data is None:
            return False
        self.global_dirty = True
        if self._atomic_write(self.global_path, data):
            self.global_dirty = False
            return True
        return False

    def unlocked_characters(self) -> list[str]:
        return list(self.global_cache["unlocked_characters"])

    def unlocked_weapons(self) -> list[str]:
        return list(self.global_cache["unlocked_weapons"])

    def wizard_portals(self) -> list[str]:
        return list(self.global_cache["wizard_portals"])

    def unlock_wizard_portal(self, portal_id: str) -> bool:
        portal_id = str(portal_id)
        if portal_id in self.global_cache["wizard_portals"]:
            return False
        self.global_cache["wizard_portals"].append(portal_id)
        self.save_global()
        return True

    def settings(self) -> dict[str, float]:
        return dict(self.global_cache["settings"])

    def set_setting(self, name: str, value: float) -> float:
        if name not in DEFAULT_GLOBAL_SAVE["settings"]:
            raise KeyError(name)
        value = max(0.0, min(1.0, round(float(value), 2)))
        self.global_cache["settings"][name] = value
        self.save_global()
        return value

    def unlock_character(self, character: str) -> bool:
        character = str(character)
        if character in self.global_cache["unlocked_characters"]:
            return False
        self.global_cache["unlocked_characters"].append(character)
        self.save_global()
        return True

    def unlock_weapon(self, weapon_id: str) -> bool:
        weapon_id = str(weapon_id)
        if weapon_id in self.global_cache["unlocked_weapons"]:
            return False
        self.global_cache["unlocked_weapons"].append(weapon_id)
        self.save_global()
        return True

    def path_for(self, character: str) -> Path:
        return self.root / f"{_safe_name(character, 'character')}.json"

    def load(self, character: str) -> dict:
        if character in self.cache:
            return self.cache[character]
        data = deepcopy(DEFAULT_SAVE)
        path = self.path_for(character)
        if not path.exists() and character in LEGACY_CHARACTERS:
            legacy_path = self.path_for(LEGACY_CHARACTERS[character])
            if legacy_path.exists():
                try:
                    path.write_text(legacy_path.read_text(encoding="utf-8"), encoding="utf-8")
                except OSError:
                    pass
        try:
            loaded = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                for key in data:
                    if key in loaded:
                        if isinstance(data[key], dict) and isinstance(loaded[key], dict):
                            data[key].update(loaded[key])
                        else:
                            data[key] = loaded[key]
        except (OSError, ValueError, TypeError):
            pass
        data["character"] = character
        data["version"] = SAVE_VERSION
        for key in ("unlocked_pets", "unlocked_levels", "completed_levels"):
            data[key] = list(dict.fromkeys(str(item) for item in data.get(key, [])))
        if "home_castle" not in data["unlocked_levels"]:
            data["unlocked_levels"].insert(0, "home_castle")
        # Campaign v2 inserts Castle Keep between Home Castle and the older map.
        if (
            "home_castle" in data["completed_levels"]
            or "blacksmith" in data["unlocked_levels"]
            or "arena" in data["unlocked_levels"]
        ) and "castle_keep" not in data["unlocked_levels"]:
            data["unlocked_levels"].append("castle_keep")
        if "castle_keep" in data["completed_levels"] and "barbarian_war" not in data["unlocked_levels"]:
            data["unlocked_levels"].append("barbarian_war")
        if "barbarian_war" in data["completed_levels"] and "barbarian_boss" not in data["unlocked_levels"]:
            data["unlocked_levels"].append("barbarian_boss")
        if "barbarian_boss" in data["completed_levels"] and "forest_entrance" not in data["unlocked_levels"]:
            data["unlocked_levels"].append("forest_entrance")
        if "forest_entrance" in data["completed_levels"] and "thieves_forest" not in data["unlocked_levels"]:
            data["unlocked_levels"].append("thieves_forest")
        if "thieves_forest" in data["completed_levels"]:
            for next_level in ("thieves_store", "abandoned_mill"):
                if next_level not in data["unlocked_levels"]:
                    data["unlocked_levels"].append(next_level)
        if "abandoned_mill" in data["completed_levels"] and "rapids_ride" not in data["unlocked_levels"]:
            data["unlocked_levels"].append("rapids_ride")
        if "rapids_ride" in data["completed_levels"] and "cat_fish" not in data["unlocked_levels"]:
            data["unlocked_levels"].append("cat_fish")
        if "cat_fish" in data["completed_levels"] and "tall_grass_field" not in data["unlocked_levels"]:
            data["unlocked_levels"].append("tall_grass_field")
        if "tall_grass_field" in data["completed_levels"] and "pipistrellos_cave" not in data["unlocked_levels"]:
            data["unlocked_levels"].append("pipistrellos_cave")
        if "pipistrellos_cave" in data["completed_levels"]:
            for next_level in ("industrial_castle", "flowery_field"):
                if next_level not in data["unlocked_levels"]:
                    data["unlocked_levels"].append(next_level)
        if "flowery_field" in data["completed_levels"] and "wedding_crash" not in data["unlocked_levels"]:
            data["unlocked_levels"].append("wedding_crash")
        if "wedding_crash" in data["completed_levels"]:
            for next_level in ("church_store", "parade"):
                if next_level not in data["unlocked_levels"]:
                    data["unlocked_levels"].append(next_level)
        if "parade" in data["completed_levels"] and "cyclops_cave" not in data["unlocked_levels"]:
            data["unlocked_levels"].append("cyclops_cave")
        if "barbarian_boss" in data["completed_levels"] and "dock" not in data["unlocked_levels"]:
            data["unlocked_levels"].append("dock")
        if "dock" in data["completed_levels"] and "pirate_ship" not in data["unlocked_levels"]:
            data["unlocked_levels"].append("pirate_ship")
        if "pirate_ship" in data["completed_levels"] and "deserts" not in data["unlocked_levels"]:
            data["unlocked_levels"].append("deserts")
        if "deserts" in data["completed_levels"] and "alien_ship" not in data["unlocked_levels"]:
            data["unlocked_levels"].append("alien_ship")
        if "alien_ship" in data["completed_levels"] and "desert_chase" not in data["unlocked_levels"]:
            data["unlocked_levels"].append("desert_chase")
        if "desert_chase" in data["completed_levels"] and "sand_castle_interior" not in data["unlocked_levels"]:
            data["unlocked_levels"].append("sand_castle_interior")
        if "sand_castle_interior" in data["completed_levels"] and "sand_castle_roof" not in data["unlocked_levels"]:
            data["unlocked_levels"].append("sand_castle_roof")
        if "sand_castle_roof" in data["completed_levels"] and "flooded_temple" not in data["unlocked_levels"]:
            data["unlocked_levels"].append("flooded_temple")
        if "flooded_temple" in data["unlocked_levels"] and "marsh" not in data["unlocked_levels"]:
            data["unlocked_levels"].append("marsh")
        if "flooded_temple" in data["completed_levels"] and "medusas_lair" not in data["unlocked_levels"]:
            data["unlocked_levels"].append("medusas_lair")
        if "medusas_lair" in data["completed_levels"] and "full_moon" not in data["unlocked_levels"]:
            data["unlocked_levels"].append("full_moon")
        if "full_moon" in data["completed_levels"] and "snow_world" not in data["unlocked_levels"]:
            data["unlocked_levels"].append("snow_world")
        if "snow_world" in data["completed_levels"]:
            for next_level in ("snow_store", "ice_castle"):
                if next_level not in data["unlocked_levels"]:
                    data["unlocked_levels"].append(next_level)
        # The Final Battle became its own map level.  Existing profiles that
        # already opened the fourth Wizard Castle portal keep that progress.
        if (
            "final" in self.wizard_portals()
            or "wizard_castle_interior" in data["completed_levels"]
        ) and "wizard_castle_final" not in data["unlocked_levels"]:
            data["unlocked_levels"].append("wizard_castle_final")
        if "marsh" in data["completed_levels"] and "corn_boss" not in data["unlocked_levels"]:
            data["unlocked_levels"].append("corn_boss")
        if "corn_boss" in data["completed_levels"] and "swamp_village_store" not in data["unlocked_levels"]:
            data["unlocked_levels"].append("swamp_village_store")
        for item_id, limit in ITEM_LIMITS.items():
            data["items"][item_id] = max(0, min(limit, int(data["items"].get(item_id, 0))))
        self.cache[character] = data
        self.save(character)
        return data

    def save(self, character: str) -> bool:
        data = self.cache.get(character)
        if data is None:
            return False
        self.pending_saves.add(character)
        path = self.path_for(character)
        if self._atomic_write(path, data):
            self.pending_saves.discard(character)
            return True
        return False

    def flush(self, force=False) -> bool:
        """Retry queued saves at a controlled cadence instead of once per hit."""
        now = time.monotonic()
        if not force and now < self.next_flush_at:
            return not self.pending_saves and not self.global_dirty
        self.next_flush_at = now + .5
        if self.global_dirty:
            self.save_global()
        for character in tuple(self.pending_saves):
            self.save(character)
        return not self.pending_saves and not self.global_dirty

    def unlock_item(self, character: str, collection: str, item_id: str) -> bool:
        if collection != "pets":
            return self.unlock_weapon(item_id)
        key = "unlocked_pets"
        data = self.load(character)
        if item_id in data[key]:
            return False
        data[key].append(item_id)
        self.save(character)
        return True

    def equip(self, character: str, collection: str, item_id: str | None) -> None:
        data = self.load(character)
        data["equipped_pet" if collection == "pets" else "equipped_weapon"] = item_id
        self.save(character)

    def ensure_starting_weapon(self, character: str, weapon_id: str) -> None:
        data = self.load(character)
        self.unlock_weapon(weapon_id)
        changed = False
        if not data.get("equipped_weapon"):
            data["equipped_weapon"] = weapon_id
            changed = True
        if changed:
            self.save(character)

    @staticmethod
    def xp_needed(level: int) -> int:
        return 18 + max(1, int(level)) * 12

    def add_xp(self, character: str, amount: int) -> int:
        data = self.load(character)
        data["xp"] = int(data.get("xp", 0)) + max(0, int(amount))
        gained = 0
        while data["xp"] >= self.xp_needed(data["level"]):
            data["xp"] -= self.xp_needed(data["level"])
            data["level"] += 1
            data["stat_points"] += 1
            gained += 1
        if gained:
            self.save(character)
        elif amount:
            self.pending_saves.add(character)
        return gained

    def spend_stat(self, character: str, stat: str) -> bool:
        data = self.load(character)
        if stat not in data["attributes"] or int(data.get("stat_points", 0)) <= 0:
            return False
        data["attributes"][stat] = int(data["attributes"].get(stat, 0)) + 1
        data["stat_points"] -= 1
        self.save(character)
        return True

    def add_gold(self, character: str, amount: int) -> None:
        data = self.load(character)
        data["gold"] = max(0, int(data.get("gold", 0)) + int(amount))
        self.save(character)

    def buy(self, character: str, item_id: str, cost: int, maximum: int | None = None) -> bool:
        data = self.load(character)
        if int(data.get("gold", 0)) < int(cost):
            return False
        if item_id in data["items"]:
            current = int(data["items"].get(item_id, 0))
            item_limit = ITEM_LIMITS.get(item_id)
            if item_limit is not None:
                maximum = item_limit if maximum is None else min(int(maximum), item_limit)
            if maximum is not None and current >= maximum:
                return False
            data["items"][item_id] = current + 1
        else:
            if item_id in self.global_cache["unlocked_weapons"]:
                return False
            self.global_cache["unlocked_weapons"].append(item_id)
            self.save_global()
            data["equipped_weapon"] = item_id
        data["gold"] -= int(cost)
        self.save(character)
        return True

    def consume_item(self, character: str, item_id: str) -> bool:
        data = self.load(character)
        count = int(data["items"].get(item_id, 0))
        if count <= 0:
            return False
        data["items"][item_id] = count - 1
        self.save(character)
        return True

    def set_selected_item(self, character: str, item_id: str) -> None:
        data = self.load(character)
        if data.get("selected_item") != item_id:
            data["selected_item"] = item_id
            self.save(character)

    def autosave(self, character: str, checkpoint: str, snapshot: dict) -> None:
        """Atomically persist a live character snapshot between levels."""
        data = self.load(character)
        data["last_checkpoint"] = str(checkpoint)
        data["autosave_count"] = int(data.get("autosave_count", 0)) + 1
        data["health"] = max(0, int(snapshot.get("health", data.get("health") or 0)))
        data["equipped_weapon"] = str(snapshot.get("weapon", data["equipped_weapon"]))
        data["equipped_pet"] = snapshot.get("pet", data.get("equipped_pet"))
        selected = str(snapshot.get("selected_item", data.get("selected_item", "health_potion")))
        if selected in data["items"]:
            data["selected_item"] = selected
        for key, value in snapshot.get("items", {}).items():
            if key in data["items"]:
                data["items"][key] = max(0, int(value))
        for key, value in snapshot.get("attributes", {}).items():
            if key in data["attributes"]:
                data["attributes"][key] = max(0, int(value))
        self.save(character)

    def complete_level(self, character: str, level_id: str, unlocks: list[str]) -> None:
        data = self.load(character)
        if level_id not in data["completed_levels"]:
            data["completed_levels"].append(level_id)
        for next_level in unlocks:
            if next_level not in data["unlocked_levels"]:
                data["unlocked_levels"].append(next_level)
        self.save(character)

    def level_unlocked(self, characters: list[str], level_id: str) -> bool:
        return bool(characters) and all(level_id in self.load(name)["unlocked_levels"] for name in characters)
