"""Audit all data-driven and statically referenced source textures.

This exits non-zero when an artwork definition points at a missing/corrupt PNG,
when a JSON animation rig references a missing part, or when a level background
style lacks an editable source backdrop.  Use ``--write-manifest`` to refresh
``assets/texture_manifest.json`` after a successful audit.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame


GAME_DIR = Path(__file__).resolve().parents[1]
ASSETS = GAME_DIR / "assets"
PARTS = ("head", "body", "arm_left", "arm_right", "leg_left", "leg_right")
ITEMS = ("health_potion", "bow", "sandwich", "bomb", "horn")
PETS = (
    "bat", "cardinal", "owlet", "rammy", "seahorse", "troll", "monkey", "spiny",
    "zebra", "tiger", "snail", "pig", "yeti", "fox", "blue_ox", "cat",
)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def literal(node):
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None


def safe_style(value: str):
    return "".join(character if character.isalnum() or character in "_-" else "_" for character in value)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-manifest", action="store_true")
    args = parser.parse_args()
    required = set()
    errors = []

    for path in sorted((GAME_DIR / "characters").glob("*.json")):
        data = read_json(path)
        texture_dir = str(data.get("texture_dir", data["id"]))
        for part in PARTS:
            required.add(ASSETS / "characters" / texture_dir / f"{part}.png")
        magic = data.get("magic", {})
        if bool(data.get("has_magic")):
            magic_dir = str(magic.get("texture_dir", data["id"]))
            for ability in ("projectile", "splash", "jump", "infusion"):
                required.add(ASSETS / "magic" / magic_dir / f"{ability}.png")

    for path in sorted((GAME_DIR / "weapons").glob("*.json")):
        required.add(ASSETS / "weapons" / f"{read_json(path)['id']}.png")
    for key in ITEMS:
        required.add(ASSETS / "items" / f"{key}.png")
    for key in PETS:
        required.add(ASSETS / "pets" / f"{key}.png")

    rig_root = ASSETS / "art" / "rigs"
    rig_ids = set()
    for path in sorted(rig_root.glob("*/animation.json")):
        data = read_json(path)
        rig_ids.add(str(data.get("id", path.parent.name)))
        prefix = str(data.get("asset_prefix", f"rigs/{path.parent.name}/parts"))
        for animation in data.get("animations", {}).values():
            for layer in animation.get("layers", []):
                part = layer.get("part")
                if part:
                    root = ASSETS if prefix.startswith("characters/") else ASSETS / "art"
                    required.add(root / prefix / f"{part}.png")

    for path in sorted((GAME_DIR / "mounts").glob("*.json")):
        data = read_json(path)
        parts = data.get("parts", {})
        if isinstance(parts, dict) and parts:
            texture_dir = str(data.get("texture_dir", data["id"]))
            for part in parts:
                required.add(ASSETS / "mounts" / texture_dir / f"{part}.png")
        elif str(data.get("style", data["id"])) not in rig_ids:
            errors.append(f"mount {data['id']!r} has neither part PNGs nor a JSON texture rig")

    styles = set()
    for path in sorted((GAME_DIR / "levels").glob("*.json")):
        if path.name == "map.json":
            continue
        data = read_json(path)
        for scene in data.get("scenes", {}).values():
            style = str(scene.get("background", "castle_courtyard"))
            styles.add(style)
            required.add(ASSETS / "art" / "backgrounds" / f"{safe_style(style)}.png")

    tree = ast.parse((GAME_DIR / "game.py").read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        name = node.func.attr
        if name == "draw_level_image" and len(node.args) >= 2:
            level_id, key = literal(node.args[0]), literal(node.args[1])
            if level_id and key:
                required.add(ASSETS / "levels" / level_id / f"{key}.png")
        elif name == "draw_art_image" and node.args:
            key = literal(node.args[0])
            if key:
                # Character-specific extra poses are exposed through the same
                # art_image API but intentionally live beside the six limbs.
                root = ASSETS if key.startswith("characters/") else ASSETS / "art"
                required.add(root / f"{key}.png")
        elif name in {"draw_boss_image", "boss_part"} and len(node.args) >= 2:
            boss_id, part = literal(node.args[0]), literal(node.args[1])
            if boss_id and part:
                required.add(ASSETS / "bosses" / boss_id / f"{part}.png")
        elif name in {"draw_effect_image", "effect"} and len(node.args) >= 2:
            collection, key = literal(node.args[0]), literal(node.args[1])
            if collection == "story" and key:
                required.add(ASSETS / "story" / f"{key}.png")

    # Validate the complete editable library too, not only the statically
    # discoverable references. Dynamic JSON/f-string lookups are then covered
    # by both this image check and the every-scene smoke suite.
    required.update(ASSETS.rglob("*.png"))

    missing = sorted(path for path in required if not path.is_file())
    errors.extend(f"missing {path.relative_to(GAME_DIR).as_posix()}" for path in missing)

    pygame.init()
    verified = []
    for path in sorted(required):
        if not path.is_file():
            continue
        try:
            image = pygame.image.load(str(path))
            if image.get_width() < 1 or image.get_height() < 1:
                errors.append(f"empty image {path.relative_to(GAME_DIR).as_posix()}")
            else:
                verified.append(path)
        except (pygame.error, OSError) as exc:
            errors.append(f"unreadable {path.relative_to(GAME_DIR).as_posix()}: {exc}")
    pygame.quit()

    if errors:
        print("Texture coverage audit FAILED:")
        for error in errors:
            print(f"  - {error}")
        raise SystemExit(1)

    manifest = {
        "format": 1,
        "coverage": {
            "required_pngs": len(required),
            "verified_pngs": len(verified),
            "background_styles": len(styles),
            "animation_rigs": len(rig_ids),
        },
        "procedural_runtime_only": [
            "text and numeric labels",
            "health, mana, timer, and progress-bar fill amounts",
            "selection, collision, and tutorial guides",
            "particle positions, screen fades, glow, weather, and camera shake",
        ],
        "textures": sorted(path.relative_to(GAME_DIR).as_posix() for path in verified),
    }
    if args.write_manifest:
        output = ASSETS / "texture_manifest.json"
        output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {output.relative_to(GAME_DIR).as_posix()}")
    print(
        f"Texture coverage passed: {len(verified)} PNGs, {len(styles)} background styles, "
        f"and {len(rig_ids)} part rigs verified."
    )


if __name__ == "__main__":
    main()
