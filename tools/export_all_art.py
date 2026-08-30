"""Export legacy pygame vector artwork into editable, runtime-loaded PNGs.

The game intentionally bypasses PNG loading while this tool runs. Existing PNGs
are preserved unless --force is supplied, so repainting an exported asset is safe.
Run from the SDBox root with:

    py games/castle_crashers_terrible_edition/tools/export_all_art.py
"""

from __future__ import annotations

import argparse
import math
import os
import sys
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ["SDBOX_EXPORT_VECTOR_ART"] = "1"

import pygame

GAME_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GAME_DIR))

from game import Game  # noqa: E402


CANVAS_SIZE = 640
ORIGIN = (CANVAS_SIZE // 2, CANVAS_SIZE // 2)
ART_ROOT = GAME_DIR / "assets" / "art"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="overwrite existing PNGs")
    args = parser.parse_args()

    pygame.init()
    game = Game(smoke_test=True)
    game.canvas = pygame.Surface((CANVAS_SIZE, CANVAS_SIZE), pygame.SRCALPHA)

    jobs: list[tuple[str, object, float]] = [
        ("actors/troll", lambda: game.draw_troll_creature(ORIGIN), 0),
        ("actors/troll_skeleton", lambda: game.draw_troll_creature(ORIGIN, skeleton=True), 0),
        ("actors/troll_boss", lambda: game.draw_troll_creature(ORIGIN, boss=True), 0),
        ("actors/black_slime", lambda: game.draw_black_slime(ORIGIN), 0),
        ("actors/beekeeper_idle", lambda: game.draw_beekeeper_actor(ORIGIN, facing=1), 0),
        ("actors/beekeeper_attack", lambda: game.draw_beekeeper_actor(ORIGIN, facing=1, attacking=True), 0),
        ("actors/bag_head", lambda: game.draw_bag_head(*ORIGIN), 0),
        ("actors/cyclops_angry", lambda: game.draw_cyclops_actor(ORIGIN, facing=1, crying=False), 0),
        ("actors/cyclops_crying", lambda: game.draw_cyclops_actor(ORIGIN, facing=1, crying=True), 0),
        ("actors/white_princess", lambda: game.draw_white_princess(ORIGIN, facing=1), 0),
        ("actors/white_princess_crying", lambda: game.draw_white_princess(ORIGIN, facing=1, crying=True), 0),
        ("actors/white_princess_happy", lambda: game.draw_white_princess(ORIGIN, facing=1, happy=True), 0),
        ("actors/owl", lambda: game.draw_owl_actor(ORIGIN), 0),
        ("actors/owl_scared", lambda: game.draw_owl_actor(ORIGIN, scared=1), 0),
        ("actors/bear", lambda: game.draw_bear_actor(ORIGIN), 0),
        ("actors/bear_scared", lambda: game.draw_bear_actor(ORIGIN, scared=1), 0),
        ("actors/blue_bird", lambda: game.draw_blue_bird(ORIGIN, facing=1), 0),
        ("props/rapids_dino_head", lambda: game.draw_rapids_object({"id": 0, "x": ORIGIN[0], "y": ORIGIN[1] + 1, "fall_z": 1, "kind": "dino_head", "platform": False}), 0),
        ("props/rapids_rock", lambda: game.draw_rapids_object({"id": 0, "x": ORIGIN[0], "y": ORIGIN[1] + 1, "fall_z": 1, "kind": "rock", "platform": False}), 0),
        ("props/shark_fin", lambda: game.draw_shark_fin({"x": ORIGIN[0], "y": ORIGIN[1], "direction": 1, "phase": "attack"}), 0),
        ("props/paw_flag", lambda: game.draw_paw_flag(*ORIGIN), 0),
        ("props/arrow_machine", lambda: game.draw_arrow_machine(*ORIGIN, facing=1), 0),
        ("props/bush_entrance", lambda: game.draw_bush_entrance(*ORIGIN), 0),
        ("props/siege_machine", lambda: game.draw_siege_machine(*ORIGIN), 0),
        ("props/siege_machine_open", lambda: game.draw_siege_machine(*ORIGIN, open_hatch=True), 0),
        ("pickups/gold_bag", lambda: game.draw_gold_bag(ORIGIN), 0),
    ]

    flower_colors = {
        "pink": (247, 113, 171), "yellow": (247, 207, 65),
        "white": (221, 237, 243), "blue": (116, 180, 244),
        "purple": (151, 102, 205), "orange": (238, 128, 78),
    }
    for name, color in flower_colors.items():
        jobs.append((f"props/flower_{name}", lambda color=color: game.draw_flower(*ORIGIN, color=color), 0))
    for kind in ("banana", "pear", "cherry", "meat", "apple"):
        jobs.append((f"pickups/food_{kind}", lambda kind=kind: game.draw_food_icon(kind, ORIGIN), 0))

    written = 0
    kept = 0
    for relative_name, draw, elapsed in jobs:
        output = ART_ROOT / f"{relative_name}.png"
        if output.is_file() and not args.force:
            kept += 1
            continue
        output.parent.mkdir(parents=True, exist_ok=True)
        game.canvas.fill((0, 0, 0, 0))
        game.elapsed = float(elapsed)
        draw()
        pygame.image.save(game.canvas, str(output))
        written += 1

    def export_centered(relative_name, draw, anchor, output_size=640, canvas_size=(1280, 960), erase_rects=()):
        nonlocal written, kept
        output = ART_ROOT / f"{relative_name}.png"
        if output.is_file() and not args.force:
            kept += 1
            return
        output.parent.mkdir(parents=True, exist_ok=True)
        game.canvas = pygame.Surface(canvas_size, pygame.SRCALPHA)
        game.canvas.fill((0, 0, 0, 0))
        draw()
        asset = pygame.Surface((output_size, output_size), pygame.SRCALPHA)
        asset.blit(game.canvas, (output_size // 2 - int(anchor[0]), output_size // 2 - int(anchor[1])))
        for relative_rect in erase_rects:
            erase = pygame.Rect(relative_rect)
            erase.move_ip(output_size // 2, output_size // 2)
            asset.fill((0, 0, 0, 0), erase)
        pygame.image.save(asset, str(output))
        written += 1

    # Tall props are captured around their gameplay anchor instead of being
    # cropped, so repainting never changes where a doorway or machine sits.
    export_centered("props/giant_stone_arch", lambda: game.draw_giant_stone_arch(640, 620, False), (640, 620), 1024, (1280, 1100))
    export_centered("props/giant_stone_arch_label", lambda: game.draw_giant_stone_arch(640, 620, True), (640, 620), 1024, (1280, 1100))

    game.set_state("thieves_forest")
    game.level_runtime.camera_x = 0
    world_x = 640.0
    for variant, kwargs in (
        ("plain", {}), ("flowers", {"flowers": True}), ("dark", {"dark_center": True}),
    ):
        anchor = (game.level_runtime.screen_x(world_x), game.world_screen_y(world_x, 520))
        export_centered(
            f"props/forest_bush_{variant}",
            lambda kwargs=kwargs: game.draw_forest_bush(world_x, **kwargs),
            anchor,
        )
    pillar_anchor = (game.level_runtime.screen_x(world_x), game.world_screen_y(world_x, 505))
    export_centered("props/ruin_pillar_intact", lambda: game.draw_ruin_pillar(world_x), pillar_anchor)
    export_centered("props/ruin_pillar_broken", lambda: game.draw_ruin_pillar(world_x, True), pillar_anchor)

    game.set_state("pipistrellos_cave")
    game.level_runtime.camera_x = 0
    skeleton_anchor = (game.level_runtime.screen_x(world_x), game.world_screen_y(world_x, 555))
    export_centered("props/skeleton_body", lambda: game.draw_skeleton_body(world_x, 555), skeleton_anchor)

    game.set_state("tall_grass_field")
    game.level_runtime.camera_x = 0
    house_anchor = (game.level_runtime.screen_x(world_x), game.world_screen_y(world_x, 510))
    export_centered("props/grass_house", lambda: game.draw_grass_house(world_x), house_anchor)
    catapult_anchor = (game.level_runtime.screen_x(world_x), game.world_screen_y(world_x, 540))
    for frame in range(8):
        angle = -80 + frame / 7 * 100
        export_centered(
            f"props/catapult_empty_{frame}",
            lambda angle=angle: game.draw_catapult(world_x, arm_angle=angle), catapult_anchor,
        )
        export_centered(
            f"props/catapult_loaded_{frame}",
            lambda angle=angle: game.draw_catapult(world_x, loaded=True, arm_angle=angle), catapult_anchor,
        )

    game.set_state("thieves_forest")
    game.level_runtime.camera_x = 0
    breakable_x = 640.0
    breakable_anchor = (
        game.level_runtime.screen_x(breakable_x),
        game.world_screen_y(breakable_x, 535),
    )
    original_text = game.text
    original_item = game.draw_item_image
    original_food = game.draw_food_icon
    original_troll = game.draw_troll_creature
    game.text = lambda *unused, **unused_kwargs: None
    breakable_jobs = (
        ("chest", "props/chest"),
        ("secret_wall", "props/secret_wall"),
        ("sandwich_door", "props/sandwich_door"),
        ("lava_statue", "props/lava_statue"),
        ("church_window", "props/church_window"),
        ("banquet_table", "props/banquet_table"),
        ("mushroom", "props/mushroom"),
        ("fortress_gate", "props/fortress_gate"),
        ("breakable_wall", "props/breakable_wall"),
    )
    for kind, art_key in breakable_jobs:
        game.scene_breakables = [{
            "id": f"export_{kind}", "kind": kind, "x": breakable_x, "y": 535,
            "health": 100, "max_health": 100, "output": {"kind": "apple"},
        }]
        game.draw_item_image = (lambda *unused, **unused_kwargs: True) if kind == "sandwich_door" else original_item
        game.draw_food_icon = (lambda *unused, **unused_kwargs: None) if kind == "banquet_table" else original_food
        game.draw_troll_creature = (lambda *unused, **unused_kwargs: None) if kind == "secret_wall" else original_troll
        erase = ((-120, 28, 240, 90),) if kind == "fortress_gate" else ()
        export_centered(
            art_key, lambda: game.draw_scene_breakables(), breakable_anchor,
            erase_rects=erase,
        )
    game.text = original_text
    game.draw_item_image = original_item
    game.draw_food_icon = original_food
    game.draw_troll_creature = original_troll
    game.scene_breakables = []

    def export_inventory_icon(collection, key, folder):
        nonlocal written, kept
        output = GAME_DIR / "assets" / folder / f"{key}.png"
        if output.is_file() and not args.force:
            kept += 1
            return
        output.parent.mkdir(parents=True, exist_ok=True)
        game.canvas = pygame.Surface((320, 320), pygame.SRCALPHA)
        game.canvas.fill((0, 0, 0, 0))
        game.draw_item_image(collection, key, (160, 160), 180)
        bounds = game.canvas.get_bounding_rect(min_alpha=1)
        image = game.canvas.subsurface(bounds).copy() if bounds.width and bounds.height else game.canvas
        pygame.image.save(image, str(output))
        written += 1

    for pet in ("bat", "seahorse", "troll", "monkey"):
        export_inventory_icon("pets", pet, "pets")
    for weapon in ("alien_hominid_weapon", "lightsaber", "walking_cane"):
        export_inventory_icon("weapons", weapon, "weapons")
    export_inventory_icon("items", "bomb", "items")

    pygame.quit()
    print(f"Art export complete: {written} PNGs written, {kept} repainted PNGs preserved.")


if __name__ == "__main__":
    main()
