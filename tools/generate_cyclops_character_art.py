"""Generate the six editable PNG limbs for the playable Cyclops.

Existing files are preserved unless ``--force`` is supplied.  This keeps any
hand-painted replacements safe while still making a fresh checkout complete.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame


GAME_DIR = Path(__file__).resolve().parents[1]
OUTPUT = GAME_DIR / "assets" / "characters" / "cyclops"
INK = (8, 15, 24)
SKIN = (105, 82, 67)
SKIN_LIGHT = (145, 111, 78)
LEATHER = (74, 48, 39)
GOLD = (225, 169, 54)
CREAM = (248, 239, 213)


def outlined_polygon(surface, points, color, width=7):
    pygame.draw.polygon(surface, INK, points)
    center_x = sum(point[0] for point in points) / len(points)
    center_y = sum(point[1] for point in points) / len(points)
    inset = []
    for x, y in points:
        distance = max(1.0, ((x - center_x) ** 2 + (y - center_y) ** 2) ** .5)
        inset.append((x + (center_x - x) * width / distance, y + (center_y - y) * width / distance))
    pygame.draw.polygon(surface, color, inset)


def head():
    surface = pygame.Surface((156, 140), pygame.SRCALPHA)
    pygame.draw.ellipse(surface, INK, (10, 10, 136, 124))
    pygame.draw.ellipse(surface, SKIN, (19, 19, 118, 106))
    pygame.draw.ellipse(surface, INK, (29, 45, 98, 54))
    pygame.draw.ellipse(surface, CREAM, (38, 52, 80, 39))
    pygame.draw.ellipse(surface, GOLD, (49, 58, 58, 27))
    pygame.draw.circle(surface, INK, (86, 71), 10)
    pygame.draw.line(surface, INK, (43, 42), (113, 35), 9)
    pygame.draw.arc(surface, INK, (47, 92, 63, 25), .15, 2.99, 7)
    return surface


def body():
    surface = pygame.Surface((120, 140), pygame.SRCALPHA)
    outlined_polygon(surface, [(13, 18), (60, 3), (107, 18), (115, 108), (89, 136), (31, 136), (5, 108)], SKIN, 8)
    pygame.draw.polygon(surface, LEATHER, [(19, 27), (101, 27), (91, 102), (29, 102)])
    pygame.draw.line(surface, GOLD, (29, 69), (91, 69), 7)
    pygame.draw.circle(surface, INK, (60, 50), 19)
    pygame.draw.ellipse(surface, CREAM, (46, 41, 28, 17))
    pygame.draw.circle(surface, INK, (63, 49), 5)
    pygame.draw.rect(surface, INK, (9, 101, 102, 25), border_radius=7)
    pygame.draw.rect(surface, GOLD, (17, 108, 86, 10), border_radius=4)
    return surface


def arm(right=False):
    surface = pygame.Surface((62, 104), pygame.SRCALPHA)
    points = [(11, 4), (48, 10), (59, 63), (44, 99), (14, 93), (3, 57)]
    if right:
        points = [(62 - x, y) for x, y in points]
    outlined_polygon(surface, points, SKIN, 7)
    pygame.draw.line(surface, SKIN_LIGHT, (9, 61), (53, 65), 7)
    pygame.draw.circle(surface, INK, (31, 89), 13)
    pygame.draw.circle(surface, SKIN_LIGHT, (31, 89), 7)
    return surface


def leg(right=False):
    surface = pygame.Surface((64, 105), pygame.SRCALPHA)
    x = 17 if right else 13
    pygame.draw.rect(surface, INK, (x, 3, 34, 73), border_radius=13)
    pygame.draw.rect(surface, LEATHER, (x + 6, 9, 22, 60), border_radius=9)
    pygame.draw.rect(surface, GOLD, (x + 4, 39, 26, 9), border_radius=3)
    boot = pygame.Rect(9 if right else 3, 70, 55, 29)
    pygame.draw.ellipse(surface, INK, boot)
    pygame.draw.ellipse(surface, LEATHER, boot.inflate(-8, -8))
    return surface


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="overwrite repainted Cyclops PNGs")
    args = parser.parse_args()
    pygame.init()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    images = {
        "head": head(),
        "body": body(),
        "arm_left": arm(False),
        "arm_right": arm(True),
        "leg_left": leg(False),
        "leg_right": leg(True),
    }
    written = kept = 0
    for name, image in images.items():
        path = OUTPUT / f"{name}.png"
        if path.is_file() and not args.force:
            kept += 1
            continue
        pygame.image.save(image, str(path))
        written += 1
    pygame.quit()
    print(f"Cyclops art complete: {written} PNGs written, {kept} repainted PNGs preserved.")


if __name__ == "__main__":
    main()
