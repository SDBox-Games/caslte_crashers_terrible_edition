"""Generate the original menu scenes and component knight textures.

Run with:
    py generate_assets.py

The generated PNG files are deliberately kept separate so artists can replace
any body part or menu scene without changing the game code.
"""

from __future__ import annotations

import math
import os
from pathlib import Path


os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame


APP_DIR = Path(__file__).resolve().parent
CHARACTER_DIR = APP_DIR / "assets" / "characters"
PICTURE_DIR = APP_DIR / "pictures" / "main_menu"
INK = (8, 14, 22)
STEEL = (172, 188, 197)
LIGHT_STEEL = (225, 234, 232)
GOLD = (241, 182, 61)

PALETTES = {
    "ember": ((190, 57, 42), (255, 132, 36), (255, 92, 42), "flame"),
    "tide": ((39, 100, 174), (72, 196, 224), (70, 229, 255), "wave"),
    "grove": ((54, 124, 70), (139, 202, 75), (136, 246, 141), "leaf"),
    "storm": ((105, 67, 157), (205, 144, 250), (227, 174, 255), "bolt"),
}


def outlined_polygon(surface, points, fill, width=6):
    pygame.draw.polygon(surface, INK, points)
    center_x = sum(point[0] for point in points) / len(points)
    center_y = sum(point[1] for point in points) / len(points)
    inset = []
    for x, y in points:
        distance = max(1.0, math.hypot(x - center_x, y - center_y))
        inset.append(
            (
                int(x + (center_x - x) * width / distance),
                int(y + (center_y - y) * width / distance),
            )
        )
    pygame.draw.polygon(surface, fill, inset)


def draw_motif(surface, motif, center, color, scale=1.0):
    x, y = center
    if motif == "flame":
        points = [
            (x, y - 22 * scale),
            (x + 14 * scale, y - 2 * scale),
            (x + 9 * scale, y + 17 * scale),
            (x, y + 23 * scale),
            (x - 13 * scale, y + 13 * scale),
            (x - 12 * scale, y - 4 * scale),
        ]
        pygame.draw.polygon(surface, color, points)
        pygame.draw.polygon(
            surface,
            (255, 221, 91),
            [(x, y - 5 * scale), (x + 5 * scale, y + 13 * scale), (x - 6 * scale, y + 13 * scale)],
        )
    elif motif == "wave":
        pygame.draw.arc(
            surface,
            color,
            pygame.Rect(x - 24 * scale, y - 18 * scale, 48 * scale, 39 * scale),
            math.pi * 0.08,
            math.pi * 1.15,
            max(2, int(8 * scale)),
        )
        pygame.draw.circle(surface, color, (int(x + 15 * scale), int(y - 5 * scale)), max(2, int(6 * scale)))
    elif motif == "leaf":
        pygame.draw.ellipse(
            surface,
            color,
            pygame.Rect(x - 16 * scale, y - 25 * scale, 31 * scale, 49 * scale),
        )
        pygame.draw.line(
            surface,
            (229, 244, 163),
            (x - 8 * scale, y + 18 * scale),
            (x + 8 * scale, y - 17 * scale),
            max(2, int(4 * scale)),
        )
    else:
        pygame.draw.polygon(
            surface,
            color,
            [
                (x + 4 * scale, y - 27 * scale),
                (x - 14 * scale, y + 1 * scale),
                (x - 2 * scale, y + 1 * scale),
                (x - 9 * scale, y + 27 * scale),
                (x + 18 * scale, y - 7 * scale),
                (x + 5 * scale, y - 7 * scale),
            ],
        )


def head_texture(name, accent, glow, motif):
    surface = pygame.Surface((144, 126), pygame.SRCALPHA)
    helmet = pygame.Rect(16, 20, 112, 98)
    pygame.draw.ellipse(surface, INK, helmet)
    pygame.draw.ellipse(surface, STEEL, helmet.inflate(-9, -9))
    pygame.draw.arc(surface, LIGHT_STEEL, helmet.inflate(-24, -19), math.pi * 0.78, math.pi * 1.55, 5)
    visor = pygame.Rect(18, 62, 108, 35)
    pygame.draw.rect(surface, INK, visor, border_radius=12)
    for eye_x in (47, 94):
        pygame.draw.ellipse(surface, glow, (eye_x - 14, 74, 28, 7))

    if motif == "flame":
        outlined_polygon(surface, [(42, 31), (51, 2), (69, 25), (88, 0), (103, 32)], accent, 5)
    elif motif == "wave":
        outlined_polygon(surface, [(25, 48), (3, 34), (19, 68)], accent, 4)
        outlined_polygon(surface, [(119, 46), (141, 31), (126, 68)], accent, 4)
    elif motif == "leaf":
        pygame.draw.line(surface, INK, (54, 30), (38, 1), 12)
        pygame.draw.line(surface, INK, (89, 29), (108, 0), 12)
        pygame.draw.line(surface, accent, (54, 30), (38, 1), 5)
        pygame.draw.line(surface, accent, (89, 29), (108, 0), 5)
        pygame.draw.ellipse(surface, accent, (24, 0, 22, 12))
        pygame.draw.ellipse(surface, accent, (101, 0, 22, 12))
    else:
        outlined_polygon(surface, [(49, 31), (61, 3), (70, 26), (86, 5), (96, 34)], accent, 4)
        pygame.draw.circle(surface, glow, (70, 11), 6)

    draw_motif(surface, motif, (71, 45), accent, 0.38)
    return surface


def body_texture(armor, accent, glow, motif):
    surface = pygame.Surface((110, 128), pygame.SRCALPHA)
    points = [(17, 14), (55, 4), (93, 14), (104, 102), (80, 122), (30, 122), (6, 102)]
    outlined_polygon(surface, points, armor, 7)
    pygame.draw.line(surface, LIGHT_STEEL, (27, 20), (20, 87), 5)
    belt = pygame.Rect(8, 90, 96, 23)
    pygame.draw.rect(surface, INK, belt, border_radius=7)
    pygame.draw.rect(surface, GOLD, belt.inflate(-7, -7), border_radius=4)
    badge = pygame.Rect(28, 30, 54, 54)
    pygame.draw.ellipse(surface, INK, badge)
    pygame.draw.ellipse(surface, (23, 35, 46), badge.inflate(-6, -6))
    draw_motif(surface, motif, badge.center, glow, 0.68)
    return surface


def arm_texture(armor, accent, side):
    surface = pygame.Surface((56, 94), pygame.SRCALPHA)
    points = [(14, 5), (43, 9), (50, 61), (37, 88), (15, 84), (5, 56)]
    if side == "right":
        points = [(56 - x, y) for x, y in points]
    outlined_polygon(surface, points, armor, 6)
    pygame.draw.line(surface, accent, (10, 52), (46, 57), 8)
    pygame.draw.circle(surface, INK, (29, 79), 13)
    pygame.draw.circle(surface, accent, (29, 79), 7)
    return surface


def leg_texture(armor, accent, side):
    surface = pygame.Surface((58, 94), pygame.SRCALPHA)
    shin_x = 14 if side == "left" else 16
    pygame.draw.rect(surface, INK, (shin_x, 3, 30, 65), border_radius=12)
    pygame.draw.rect(surface, armor, (shin_x + 5, 8, 20, 55), border_radius=9)
    pygame.draw.rect(surface, accent, (shin_x + 4, 33, 22, 9), border_radius=3)
    boot = pygame.Rect(4 if side == "left" else 10, 61, 48, 27)
    pygame.draw.ellipse(surface, INK, boot)
    pygame.draw.ellipse(surface, armor, boot.inflate(-7, -7))
    return surface


def generate_characters():
    for name, (armor, accent, glow, motif) in PALETTES.items():
        folder = CHARACTER_DIR / name
        folder.mkdir(parents=True, exist_ok=True)
        images = {
            "head.png": head_texture(name, accent, glow, motif),
            "body.png": body_texture(armor, accent, glow, motif),
            "arm_left.png": arm_texture(armor, accent, "left"),
            "arm_right.png": arm_texture(armor, accent, "right"),
            "leg_left.png": leg_texture(armor, accent, "left"),
            "leg_right.png": leg_texture(armor, accent, "right"),
        }
        for filename, image in images.items():
            pygame.image.save(image, str(folder / filename))


def gradient(surface, top, bottom):
    width, height = surface.get_size()
    for y in range(height):
        amount = y / max(1, height - 1)
        color = tuple(int(a + (b - a) * amount) for a, b in zip(top, bottom))
        pygame.draw.line(surface, color, (0, y), (width, y))


def castle_scene():
    surface = pygame.Surface((1280, 720))
    gradient(surface, (29, 52, 82), (235, 122, 72))
    pygame.draw.circle(surface, (255, 222, 142), (1010, 142), 90)
    pygame.draw.polygon(surface, (42, 54, 65), [(0, 485), (230, 285), (425, 475), (650, 310), (920, 470), (1280, 265), (1280, 720), (0, 720)])
    for x, width, height in ((760, 150, 235), (910, 230, 310), (1100, 130, 210)):
        pygame.draw.rect(surface, (20, 28, 38), (x, 720 - height, width, height))
        for tooth in range(4):
            pygame.draw.rect(surface, (20, 28, 38), (x + tooth * width // 4, 720 - height - 35, width // 7, 38))
    pygame.draw.polygon(surface, (72, 104, 71), [(0, 575), (310, 470), (650, 590), (980, 485), (1280, 570), (1280, 720), (0, 720)])
    return surface


def frog_scene():
    surface = pygame.Surface((1280, 720))
    gradient(surface, (22, 80, 84), (102, 168, 118))
    pygame.draw.circle(surface, (204, 238, 187), (1040, 115), 72)
    for x, y, radius in ((155, 145, 90), (295, 102, 115), (485, 162, 100), (1170, 185, 125)):
        pygame.draw.circle(surface, (21, 62, 55), (x, y), radius)
    pygame.draw.ellipse(surface, (55, 119, 69), (600, 315, 470, 330))
    pygame.draw.circle(surface, (55, 119, 69), (705, 336), 94)
    pygame.draw.circle(surface, (55, 119, 69), (963, 336), 94)
    pygame.draw.circle(surface, (238, 226, 170), (705, 335), 34)
    pygame.draw.circle(surface, (238, 226, 170), (963, 335), 34)
    pygame.draw.circle(surface, INK, (705, 337), 15)
    pygame.draw.circle(surface, INK, (963, 337), 15)
    pygame.draw.ellipse(surface, INK, (740, 416, 185, 94))
    pygame.draw.ellipse(surface, (160, 67, 72), (755, 437, 155, 49))
    pygame.draw.rect(surface, (42, 91, 57), (0, 580, 1280, 140))
    return surface


def arena_scene():
    surface = pygame.Surface((1280, 720))
    gradient(surface, (20, 21, 47), (102, 49, 52))
    for x in range(90, 1250, 180):
        pygame.draw.circle(surface, (255, 193, 84), (x, 175 + (x % 3) * 8), 8)
        pygame.draw.circle(surface, (246, 80, 45), (x, 175 + (x % 3) * 8), 20, 5)
    pygame.draw.ellipse(surface, (143, 102, 67), (90, 350, 1100, 440))
    pygame.draw.ellipse(surface, (222, 176, 106), (150, 390, 980, 330))
    for x in range(0, 1280, 55):
        pygame.draw.rect(surface, (25, 25, 35), (x, 295 + (x % 4) * 5, 39, 85))
        pygame.draw.circle(surface, (61, 43, 57), (x + 19, 295), 22)
    return surface


def generate_menu_pictures():
    PICTURE_DIR.mkdir(parents=True, exist_ok=True)
    scenes = {
        "01_castle_sunset.png": castle_scene(),
        "02_frog_hollow.png": frog_scene(),
        "03_arena_night.png": arena_scene(),
    }
    for filename, image in scenes.items():
        pygame.image.save(image, str(PICTURE_DIR / filename))


def main():
    pygame.init()
    pygame.display.set_mode((1, 1))
    generate_characters()
    generate_menu_pictures()
    pygame.quit()
    print("Generated character textures and rotating menu pictures.")


if __name__ == "__main__":
    main()
