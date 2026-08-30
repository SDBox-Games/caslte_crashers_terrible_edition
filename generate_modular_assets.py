"""Generate animation-ready character parts, standalone weapons, and pets.

Run from this directory with:
    py generate_modular_assets.py

Every body part and collectible is its own transparent PNG.  The runtime never
needs to crop a sprite sheet, which also makes hand-painted replacements easy.
"""

from __future__ import annotations

import math
import os
from pathlib import Path


os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame


ROOT = Path(__file__).resolve().parent / "assets"
INK = (8, 14, 22)
STEEL = (176, 187, 189)
LIGHT = (229, 234, 222)
GOLD = (239, 180, 55)

CAST = {
    "electric": ((190, 48, 45), (255, 236, 104), "bolt"),
    "ice": ((39, 100, 174), (72, 196, 224), "wave"),
    "fire": ((225, 107, 28), (255, 193, 45), "flame"),
    "green": ((54, 124, 70), (139, 202, 75), "leaf"),
    "barbarian": ((104, 66, 43), (46, 143, 143), "horns"),
    "cheese_boss": ((67, 42, 86), (229, 173, 44), "moon"),
    "king": ((48, 91, 160), (238, 184, 58), "crown"),
    "royal_guard": ((90, 109, 116), (36, 158, 159), "guard"),
}

WEAPONS = {
    "rusty_sword": ((170, 178, 176), "sword"),
    "pitchfork": ((137, 92, 55), "fork"),
    "wood_club": ((143, 91, 50), "club"),
    "dinner_fork": ((215, 217, 207), "fork"),
    "barbarian_axe": ((156, 166, 164), "axe"),
    "moon_blade": ((227, 177, 54), "sword"),
    "royal_spear": ((60, 164, 171), "spear"),
    "magic_wand": ((183, 126, 220), "wand"),
    "keep_sword": ((224, 229, 222), "sword"),
}

PETS = {
    "cardinal": ((220, 65, 59), "bird"),
    "owlet": ((163, 116, 72), "owl"),
    "rammy": ((221, 215, 190), "ram"),
}

MAGIC = {
    "electric": ((255, 230, 72), "bolt"),
    "ice": ((132, 226, 255), "ice"),
    "fire": ((255, 102, 36), "fire"),
    "green": ((102, 219, 83), "poison"),
}

PRINCESSES = {
    "princess_red": ((190, 48, 55), (231, 118, 42), (242, 208, 172)),
    "princess_green": ((48, 137, 74), (26, 28, 32), (213, 178, 144)),
    "princess_blue": ((49, 105, 185), (241, 213, 118), (242, 207, 173)),
    "princess_orange": ((225, 111, 30), (115, 65, 132), (221, 183, 154)),
}


def _save(surface: pygame.Surface, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pygame.image.save(surface, str(path))


def _poly(surface, points, fill, width=7):
    pygame.draw.polygon(surface, INK, points)
    cx = sum(x for x, _ in points) / len(points)
    cy = sum(y for _, y in points) / len(points)
    inset = []
    for x, y in points:
        distance = max(1, math.hypot(x - cx, y - cy))
        inset.append((x + (cx - x) * width / distance, y + (cy - y) * width / distance))
    pygame.draw.polygon(surface, fill, inset)


def head(color, accent, motif):
    s = pygame.Surface((156, 140), pygame.SRCALPHA)
    if motif == "horns":
        _poly(s, [(34, 54), (3, 13), (45, 35)], (226, 211, 174), 6)
        _poly(s, [(122, 54), (153, 13), (111, 35)], (226, 211, 174), 6)
        pygame.draw.ellipse(s, INK, (18, 26, 120, 105))
        pygame.draw.ellipse(s, color, (26, 34, 104, 89))
    else:
        pygame.draw.ellipse(s, INK, (18, 20, 120, 111))
        pygame.draw.ellipse(s, STEEL if motif not in {"moon", "crown"} else color, (26, 28, 104, 95))
    pygame.draw.rect(s, INK, (18, 72, 120, 35), border_radius=11)
    for x in (55, 101):
        pygame.draw.ellipse(s, accent, (x - 14, 84, 28, 7))
    if motif in {"flame", "bolt"}:
        _poly(s, [(42, 37), (55, 2), (75, 30), (97, 0), (112, 38)], accent, 5)
    elif motif in {"wave", "guard"}:
        _poly(s, [(25, 59), (2, 39), (22, 78)], accent, 5)
        _poly(s, [(131, 59), (154, 39), (134, 78)], accent, 5)
    elif motif == "leaf":
        pygame.draw.line(s, INK, (55, 35), (36, 2), 13)
        pygame.draw.line(s, INK, (101, 35), (120, 2), 13)
        pygame.draw.line(s, accent, (55, 35), (36, 2), 6)
        pygame.draw.line(s, accent, (101, 35), (120, 2), 6)
    elif motif == "moon":
        pygame.draw.arc(s, GOLD, (46, 29, 63, 53), .45, 5.2, 8)
    elif motif == "crown":
        _poly(s, [(40, 39), (46, 2), (68, 27), (80, 0), (94, 27), (116, 2), (116, 43)], GOLD, 5)
    return s


def body(color, accent, motif):
    s = pygame.Surface((120, 140), pygame.SRCALPHA)
    _poly(s, [(16, 13), (60, 4), (104, 13), (113, 110), (89, 134), (31, 134), (7, 110)], color, 8)
    pygame.draw.rect(s, INK, (9, 99, 102, 25), border_radius=7)
    pygame.draw.rect(s, GOLD, (16, 106, 88, 11), border_radius=4)
    pygame.draw.ellipse(s, INK, (33, 31, 54, 55))
    pygame.draw.ellipse(s, (25, 34, 43), (40, 38, 40, 41))
    if motif == "moon":
        pygame.draw.circle(s, accent, (60, 59), 17)
        pygame.draw.circle(s, (25, 34, 43), (68, 52), 14)
        for p in ((52, 62), (60, 48), (63, 68)):
            pygame.draw.circle(s, (160, 126, 52), p, 2)
    elif motif == "crown":
        _poly(s, [(47, 66), (48, 45), (57, 56), (63, 42), (71, 56), (74, 45), (74, 68)], GOLD, 3)
    else:
        pygame.draw.polygon(s, accent, [(60, 40), (73, 58), (60, 77), (47, 58)])
    return s


def arm(color, accent, right=False):
    s = pygame.Surface((62, 104), pygame.SRCALPHA)
    points = [(13, 5), (46, 10), (56, 66), (40, 98), (15, 92), (4, 61)]
    if right:
        points = [(62 - x, y) for x, y in points]
    _poly(s, points, color, 7)
    pygame.draw.line(s, accent, (10, 61), (52, 66), 8)
    pygame.draw.circle(s, INK, (31, 89), 13)
    pygame.draw.circle(s, accent, (31, 89), 7)
    return s


def leg(color, accent, right=False):
    s = pygame.Surface((64, 105), pygame.SRCALPHA)
    x = 17 if right else 13
    pygame.draw.rect(s, INK, (x, 3, 34, 73), border_radius=13)
    pygame.draw.rect(s, color, (x + 6, 9, 22, 60), border_radius=9)
    pygame.draw.rect(s, accent, (x + 4, 39, 26, 9), border_radius=3)
    boot = pygame.Rect(9 if right else 3, 70, 55, 29)
    pygame.draw.ellipse(s, INK, boot)
    pygame.draw.ellipse(s, color, boot.inflate(-8, -8))
    return s


def weapon(color, kind):
    s = pygame.Surface((96, 190), pygame.SRCALPHA)
    if kind == "club":
        pygame.draw.line(s, INK, (35, 164), (59, 31), 31)
        pygame.draw.line(s, color, (35, 164), (59, 31), 20)
        for y in (43, 66, 89):
            pygame.draw.circle(s, INK, (62, y), 7)
    else:
        pygame.draw.line(s, INK, (48, 166), (48, 60), 13)
        pygame.draw.line(s, (112, 74, 45), (48, 166), (48, 91), 7)
        if kind == "fork":
            pygame.draw.line(s, color, (48, 92), (48, 27), 9)
            for x in (34, 48, 62):
                pygame.draw.line(s, INK, (x, 39), (x, 12), 9)
                pygame.draw.line(s, color, (x, 39), (x, 12), 4)
        elif kind in {"axe"}:
            _poly(s, [(46, 68), (24, 24), (2, 40), (18, 83), (46, 78)], color, 6)
        elif kind == "spear":
            _poly(s, [(48, 4), (66, 40), (48, 61), (30, 40)], color, 5)
        elif kind == "wand":
            pygame.draw.circle(s, INK, (48, 22), 22)
            pygame.draw.circle(s, color, (48, 22), 14)
            pygame.draw.circle(s, LIGHT, (43, 17), 4)
        else:
            _poly(s, [(48, 3), (66, 91), (48, 111), (30, 91)], color, 6)
        pygame.draw.line(s, INK, (21, 112), (75, 112), 12)
        pygame.draw.line(s, GOLD, (23, 112), (73, 112), 5)
    return s


def pet(color, kind):
    s = pygame.Surface((130, 112), pygame.SRCALPHA)
    if kind == "bird":
        pygame.draw.ellipse(s, INK, (8, 38, 45, 43))
        pygame.draw.ellipse(s, color, (16, 45, 31, 28))
        pygame.draw.ellipse(s, INK, (77, 38, 45, 43))
        pygame.draw.ellipse(s, color, (83, 45, 31, 28))
    elif kind == "ram":
        pygame.draw.arc(s, INK, (2, 13, 50, 62), 1.2, 5.3, 10)
        pygame.draw.arc(s, INK, (78, 13, 50, 62), -2.2, 2.0, 10)
        pygame.draw.arc(s, (177, 151, 105), (5, 17, 43, 54), 1.2, 5.3, 5)
        pygame.draw.arc(s, (177, 151, 105), (82, 17, 43, 54), -2.2, 2.0, 5)
    else:
        _poly(s, [(31, 43), (18, 4), (55, 29)], color, 6)
        _poly(s, [(99, 43), (112, 4), (75, 29)], color, 6)
    pygame.draw.ellipse(s, INK, (28, 25, 74, 75))
    pygame.draw.ellipse(s, color, (36, 33, 58, 59))
    for x in (53, 78):
        pygame.draw.circle(s, LIGHT, (x, 57), 8)
        pygame.draw.circle(s, INK, (x, 58), 4)
    pygame.draw.polygon(s, GOLD, [(65, 65), (75, 71), (65, 77), (55, 71)])
    return s


def magic_texture(color, element, kind):
    size = 176 if kind == "splash" else 128
    s = pygame.Surface((size, size), pygame.SRCALPHA)
    cx = cy = size // 2
    outline = max(5, size // 22)
    if element == "bolt":
        points = [(cx + 10, 7), (cx - 34, cy - 3), (cx - 7, cy + 1), (cx - 27, size - 8), (cx + 39, cy - 12), (cx + 8, cy - 12)]
        _poly(s, points, color, outline)
    elif element == "ice":
        _poly(s, [(cx, 5), (cx + 39, cy - 16), (cx + 24, size - 12), (cx, size - 2), (cx - 31, size - 14), (cx - 40, cy - 19)], color, outline)
        pygame.draw.line(s, LIGHT, (cx, 16), (cx - 11, size - 25), 5)
    elif element == "fire":
        _poly(s, [(cx, 5), (cx + 30, cy - 8), (cx + 43, size - 24), (cx, size - 4), (cx - 41, size - 24), (cx - 28, cy - 10)], color, outline)
        pygame.draw.polygon(s, (255, 218, 74), [(cx, 34), (cx + 17, size - 28), (cx, size - 16), (cx - 17, size - 28)])
    else:
        pygame.draw.circle(s, INK, (cx, cy), size // 2 - 5)
        pygame.draw.circle(s, color, (cx, cy), size // 2 - 13)
        for ox, oy, radius in ((-20, -16, 10), (20, -7, 8), (4, 23, 12)):
            pygame.draw.circle(s, (190, 241, 91), (cx + ox, cy + oy), radius)
    if kind == "splash":
        for angle in range(0, 360, 45):
            dx = math.cos(math.radians(angle)) * 70
            dy = math.sin(math.radians(angle)) * 70
            pygame.draw.circle(s, INK, (int(cx + dx), int(cy + dy)), 13)
            pygame.draw.circle(s, color, (int(cx + dx), int(cy + dy)), 8)
    elif kind == "jump":
        pygame.draw.arc(s, LIGHT, (12, 12, size - 24, size - 24), .2, 2.9, 7)
    elif kind == "infusion":
        pygame.draw.circle(s, LIGHT, (cx, cy), size // 2 - 9, 6)
    return s


def princess_head(dress, hair, skin, style):
    s = pygame.Surface((156, 140), pygame.SRCALPHA)
    pygame.draw.ellipse(s, INK, (21, 18, 114, 114))
    pygame.draw.ellipse(s, hair, (28, 24, 100, 104))
    pygame.draw.ellipse(s, INK, (36, 35, 84, 88))
    pygame.draw.ellipse(s, skin, (43, 42, 70, 75))
    pygame.draw.polygon(s, hair, [(31, 54), (50, 19), (70, 43), (91, 18), (126, 55), (107, 49), (96, 65), (78, 45), (62, 66), (49, 49)])
    if style == "princess_red":
        pygame.draw.polygon(s, INK, [(34, 35), (46, 4), (65, 27), (79, 2), (94, 27), (113, 4), (123, 39)])
        pygame.draw.polygon(s, GOLD, [(42, 34), (50, 14), (67, 33), (79, 10), (93, 33), (108, 14), (116, 36)])
    else:
        # Green, blue, and orange use their requested soft cloth caps.
        pygame.draw.ellipse(s, INK, (31, 5, 94, 55))
        pygame.draw.ellipse(s, dress, (38, 12, 80, 42))
        pygame.draw.rect(s, INK, (27, 44, 106, 18), border_radius=8)
        pygame.draw.rect(s, dress, (35, 49, 90, 9), border_radius=4)
        pygame.draw.circle(s, INK, (78, 9), 12)
        pygame.draw.circle(s, dress, (78, 9), 7)
    pygame.draw.circle(s, INK, (62, 76), 4)
    pygame.draw.circle(s, INK, (93, 76), 4)
    pygame.draw.arc(s, INK, (67, 75, 22, 22), .3, 2.8, 3)
    return s


def princess_body(dress):
    s = pygame.Surface((120, 140), pygame.SRCALPHA)
    _poly(s, [(36, 6), (84, 6), (102, 120), (112, 136), (8, 136), (18, 120)], dress, 7)
    pygame.draw.rect(s, GOLD, (18, 76, 84, 15), border_radius=5)
    pygame.draw.circle(s, LIGHT, (60, 50), 11)
    return s


def item_texture(kind):
    s = pygame.Surface((128, 128), pygame.SRCALPHA)
    if kind == "potion":
        pygame.draw.rect(s, INK, (46, 13, 36, 29), border_radius=6)
        pygame.draw.rect(s, (210, 196, 151), (52, 18, 24, 19), border_radius=4)
        pygame.draw.polygon(s, INK, [(35, 38), (93, 38), (108, 105), (91, 121), (37, 121), (20, 105)])
        pygame.draw.polygon(s, (200, 43, 55), [(42, 48), (86, 48), (96, 101), (84, 112), (44, 112), (31, 101)])
        pygame.draw.line(s, LIGHT, (43, 58), (36, 91), 8)
    else:
        pygame.draw.arc(s, INK, (18, 10, 76, 110), -1.45, 1.45, 13)
        pygame.draw.arc(s, (140, 88, 49), (22, 14, 68, 102), -1.45, 1.45, 7)
        pygame.draw.line(s, LIGHT, (88, 20), (88, 111), 5)
        pygame.draw.line(s, INK, (50, 68), (116, 68), 9)
        pygame.draw.polygon(s, LIGHT, [(116, 68), (99, 57), (99, 79)])
    return s


def main():
    pygame.init()
    pygame.display.set_mode((1, 1))
    for key, (color, accent, motif) in CAST.items():
        folder = ROOT / "characters" / key
        for name, image in {
            "head": head(color, accent, motif),
            "body": body(color, accent, motif),
            "arm_left": arm(color, accent),
            "arm_right": arm(color, accent, True),
            "leg_left": leg(color, accent),
            "leg_right": leg(color, accent, True),
        }.items():
            _save(image, folder / f"{name}.png")
    for key, (color, kind) in WEAPONS.items():
        _save(weapon(color, kind), ROOT / "weapons" / f"{key}.png")
    for key, (color, kind) in PETS.items():
        _save(pet(color, kind), ROOT / "pets" / f"{key}.png")
    for key, (color, element) in MAGIC.items():
        for kind in ("projectile", "splash", "jump", "infusion"):
            _save(magic_texture(color, element, kind), ROOT / "magic" / key / f"{kind}.png")
    for key, (dress, hair, skin) in PRINCESSES.items():
        folder = ROOT / "characters" / key
        for name, image in {
            "head": princess_head(dress, hair, skin, key),
            "body": princess_body(dress),
            "arm_left": arm(dress, GOLD),
            "arm_right": arm(dress, GOLD, True),
            "leg_left": leg(dress, GOLD),
            "leg_right": leg(dress, GOLD, True),
        }.items():
            _save(image, folder / f"{name}.png")
    _save(item_texture("potion"), ROOT / "items" / "health_potion.png")
    _save(item_texture("bow"), ROOT / "items" / "bow.png")
    pygame.quit()
    print(
        f"Generated {(len(CAST) + len(PRINCESSES)) * 6} limb PNGs, "
        f"{len(WEAPONS)} weapon PNGs, {len(PETS)} pet PNGs, and {len(MAGIC) * 4} magic PNGs."
    )


if __name__ == "__main__":
    main()
