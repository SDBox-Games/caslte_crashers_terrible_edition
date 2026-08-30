"""Export one editable PNG source backdrop for every JSON background style.

The source backdrops are deliberately preserved by default.  They provide a
paintable raster source for every stage, including legacy stages whose scenery
placement is still assembled dynamically by the renderer.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
os.environ["SDBOX_EXPORT_VECTOR_ART"] = "1"

import pygame


GAME_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GAME_DIR))

from game import Game, HEIGHT, WIDTH  # noqa: E402


def safe_name(value: str) -> str:
    return "".join(character if character.isalnum() or character in "_-" else "_" for character in value)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="overwrite repainted source backdrops")
    args = parser.parse_args()
    pygame.init()
    game = Game(smoke_test=True)
    output_root = GAME_DIR / "assets" / "art" / "backgrounds"
    written = kept = 0
    seen = set()

    for level_id, config in game.level_library.levels.items():
        game.set_state(level_id)
        for scene_id, scene in config.get("scenes", {}).items():
            style = str(scene.get("background", "castle_courtyard"))
            if style in seen:
                continue
            seen.add(style)
            path = output_root / f"{safe_name(style)}.png"
            if path.is_file() and not args.force:
                kept += 1
                continue
            game.level_runtime.enter_scene(scene_id, game.players)
            game.level_runtime.camera_x = 0.0
            game.level_runtime.camera_y = 0.0
            game.canvas = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            game.canvas.fill((0, 0, 0, 0))
            game.elapsed = 0.0
            game.draw_level_background()
            path.parent.mkdir(parents=True, exist_ok=True)
            pygame.image.save(game.canvas, str(path))
            written += 1

    pygame.quit()
    print(f"Background export complete: {written} PNGs written, {kept} repainted PNGs preserved.")


if __name__ == "__main__":
    main()
