"""Generate editable magic PNGs for Necromancer and Snakey.

Existing files are preserved unless ``--force`` is supplied.
"""

from __future__ import annotations

import argparse
import math
import os
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame


GAME_DIR = Path(__file__).resolve().parents[1]
ROOT = GAME_DIR / "assets" / "magic"
INK = (8, 15, 24)
CREAM = (248, 239, 213)


def necromancer(kind):
    size = 176 if kind == "splash" else 128
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    center = pygame.Vector2(size / 2, size / 2)
    radius = size * (.39 if kind == "splash" else .31)
    pygame.draw.circle(surface, (57, 23, 76), center, int(radius + 11))
    pygame.draw.circle(surface, (158, 70, 202), center, int(radius), 7)
    pygame.draw.ellipse(surface, CREAM, (center.x - 27, center.y - 25, 54, 48))
    pygame.draw.circle(surface, INK, (int(center.x - 10), int(center.y - 5)), 7)
    pygame.draw.circle(surface, INK, (int(center.x + 10), int(center.y - 5)), 7)
    pygame.draw.polygon(surface, INK, [(center.x - 8, center.y + 7), (center.x + 8, center.y + 7), (center.x, center.y + 18)])
    for index in range(8):
        angle = index * math.tau / 8
        inner = center + pygame.Vector2(math.cos(angle), math.sin(angle)) * (radius + 5)
        outer = center + pygame.Vector2(math.cos(angle), math.sin(angle)) * (radius + 21)
        pygame.draw.line(surface, (213, 95, 255), inner, outer, 5)
    if kind == "jump":
        pygame.draw.arc(surface, CREAM, (13, 17, size - 26, size - 22), .25, math.pi - .25, 7)
    elif kind == "infusion":
        pygame.draw.circle(surface, CREAM, center, int(radius + 20), 4)
    return surface


def snakey(kind):
    size = 176 if kind == "splash" else 128
    surface = pygame.Surface((size, size), pygame.SRCALPHA)
    center_x = size // 2
    points = []
    for index in range(22):
        progress = index / 21
        x = center_x + math.sin(progress * math.tau * 1.7) * size * .18
        y = size * (.11 + progress * .73)
        points.append((x, y))
    pygame.draw.lines(surface, INK, False, points, max(15, size // 9))
    pygame.draw.lines(surface, (83, 177, 67), False, points, max(8, size // 16))
    head = points[0]
    pygame.draw.ellipse(surface, INK, (head[0] - 24, head[1] - 18, 48, 36))
    pygame.draw.ellipse(surface, (129, 220, 79), (head[0] - 18, head[1] - 12, 36, 24))
    for side in (-1, 1):
        pygame.draw.circle(surface, CREAM, (int(head[0] + side * 8), int(head[1] - 2)), 5)
        pygame.draw.circle(surface, INK, (int(head[0] + side * 8), int(head[1] - 2)), 2)
    if kind == "splash":
        pygame.draw.circle(surface, (113, 224, 86), (center_x, size // 2), int(size * .43), 8)
    elif kind == "jump":
        pygame.draw.arc(surface, CREAM, (12, 8, size - 24, size - 16), .1, math.pi - .1, 6)
    elif kind == "infusion":
        pygame.draw.circle(surface, (209, 188, 61), (center_x, size // 2), int(size * .43), 5)
    return surface


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="overwrite repainted magic PNGs")
    args = parser.parse_args()
    pygame.init()
    written = kept = 0
    for character, painter in (("necromancer", necromancer), ("snakey", snakey)):
        folder = ROOT / character
        folder.mkdir(parents=True, exist_ok=True)
        for ability in ("projectile", "splash", "jump", "infusion"):
            path = folder / f"{ability}.png"
            if path.is_file() and not args.force:
                kept += 1
                continue
            pygame.image.save(painter(ability), str(path))
            written += 1
    pygame.quit()
    print(f"Missing magic art complete: {written} PNGs written, {kept} repainted PNGs preserved.")


if __name__ == "__main__":
    main()
