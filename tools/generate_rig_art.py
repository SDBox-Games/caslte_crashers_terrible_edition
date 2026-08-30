"""Generate editable PNG parts used by the JSON animation rigs.

Existing parts are preserved unless --force is passed. Runtime animation never
draws these shapes; this headless developer tool is the one-time rasterizer.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame


GAME_DIR = Path(__file__).resolve().parents[1]
ROOT = GAME_DIR / "assets" / "art" / "rigs"
INK = (8, 15, 24)
CREAM = (248, 239, 213)
GOLD = (242, 184, 62)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="overwrite existing part PNGs")
    args = parser.parse_args()
    pygame.init()
    written = kept = 0

    def part(rig, name, painter, size=640):
        nonlocal written, kept
        path = ROOT / rig / "parts" / f"{name}.png"
        if path.is_file() and not args.force:
            kept += 1
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        painter(surface, size // 2, size // 2)
        pygame.image.save(surface, str(path))
        written += 1

    def bat_body(s, x, y):
        pygame.draw.ellipse(s, INK, (x - 20, y - 28, 40, 60))
        pygame.draw.ellipse(s, (35, 29, 38), (x - 15, y - 23, 30, 49))
        pygame.draw.polygon(s, INK, [(x - 15, y - 20), (x - 10, y - 46), (x, y - 24)])
        pygame.draw.polygon(s, INK, [(x + 15, y - 20), (x + 10, y - 46), (x, y - 24)])
        pygame.draw.circle(s, (239, 64, 56), (x + 7, y - 8), 4)

    def bat_wing(side):
        def paint(s, x, y):
            points = [(x, y), (x + side * 52, y - 17), (x + side * 38, y + 5), (x + side * 30, y + 31), (x + side * 13, y + 16)]
            pygame.draw.polygon(s, INK, points)
            pygame.draw.polygon(s, (73, 55, 70), [(x + side * 4, y + 3), (x + side * 43, y - 9), (x + side * 25, y + 23)])
        return paint

    part("small_bat", "body", bat_body)
    part("small_bat", "wing_left", bat_wing(-1))
    part("small_bat", "wing_right", bat_wing(1))

    def bee_body(s, x, y):
        pygame.draw.ellipse(s, INK, (x - 50, y - 34, 100, 69))
        pygame.draw.ellipse(s, (246, 188, 47), (x - 43, y - 27, 86, 55))
        for stripe in (-16, 9):
            pygame.draw.line(s, INK, (x + stripe, y - 25), (x + stripe, y + 25), 13)
        pygame.draw.circle(s, INK, (x + 42, y - 3), 27)
        pygame.draw.circle(s, (225, 151, 41), (x + 42, y - 3), 20)
        pygame.draw.circle(s, CREAM, (x + 49, y - 8), 7)
        pygame.draw.circle(s, INK, (x + 51, y - 8), 3)
        pygame.draw.polygon(s, INK, [(x - 53, y), (x - 86, y - 9), (x - 86, y + 9)])

    def bee_wing(s, x, y):
        pygame.draw.ellipse(s, INK, (x - 24, y - 52, 48, 58))
        pygame.draw.ellipse(s, (207, 239, 244), (x - 18, y - 46, 36, 45))

    part("bee", "body", bee_body)
    part("bee", "wing", bee_wing)

    def horse_shadow(s, x, y):
        pygame.draw.ellipse(s, (5, 10, 15, 90), (x - 105, y - 13, 210, 27))

    def horse_body(s, x, y):
        pygame.draw.ellipse(s, INK, (x - 94, y - 111, 188, 121))
        pygame.draw.ellipse(s, (139, 89, 53), (x - 86, y - 103, 172, 105))

    def horse_leg(s, x, y):
        pygame.draw.line(s, INK, (x, y), (x + 9, y + 58), 22)
        pygame.draw.line(s, (139, 89, 53), (x, y), (x + 9, y + 58), 13)
        pygame.draw.line(s, INK, (x + 9, y + 58), (x + 34, y + 61), 12)

    def horse_head(s, x, y):
        pygame.draw.line(s, INK, (x, y), (x + 30, y - 42), 49)
        pygame.draw.line(s, (139, 89, 53), (x, y), (x + 30, y - 42), 35)
        pygame.draw.ellipse(s, INK, (x - 23, y - 77, 106, 68))
        pygame.draw.ellipse(s, (205, 164, 105), (x - 15, y - 69, 90, 52))
        for ear in (-1, 1):
            ex = x + 30 + ear * 18 - 10
            pygame.draw.polygon(s, INK, [(ex, y - 66), (ex + ear * 12, y - 109), (ex + ear * 25, y - 62)])
        pygame.draw.circle(s, CREAM, (x + 48, y - 50), 7)
        pygame.draw.circle(s, INK, (x + 50, y - 50), 3)

    def horse_tail(s, x, y):
        pygame.draw.line(s, INK, (x, y), (x - 70, y - 32), 22)
        pygame.draw.line(s, (54, 35, 30), (x, y), (x - 70, y - 32), 13)

    def horse_saddle(s, x, y):
        pygame.draw.ellipse(s, INK, (x - 55, y - 21, 110, 42))
        pygame.draw.ellipse(s, (117, 38, 43), (x - 48, y - 14, 96, 29))
        pygame.draw.line(s, GOLD, (x - 40, y + 2), (x + 40, y + 2), 4)

    for name, painter in (("shadow", horse_shadow), ("body", horse_body), ("leg", horse_leg), ("head", horse_head), ("tail", horse_tail), ("saddle", horse_saddle)):
        part("horse", name, painter)

    def pip_body(s, x, y):
        pygame.draw.ellipse(s, INK, (x - 90, y - 130, 180, 250))
        pygame.draw.ellipse(s, (45, 34, 46), (x - 80, y - 120, 160, 230))
        pygame.draw.ellipse(s, (116, 76, 92), (x - 61, y - 83, 122, 96))
        for side in (-1, 1):
            pygame.draw.polygon(s, INK, [(x + side * 58, y - 93), (x + side * 76, y - 190), (x + side * 18, y - 116)])
            pygame.draw.circle(s, (245, 207, 72), (x + side * 31, y - 54), 12)
            pygame.draw.circle(s, INK, (x + side * 34, y - 54), 5)
        pygame.draw.ellipse(s, INK, (x - 43, y - 26, 86, 60))
        pygame.draw.ellipse(s, (91, 30, 42), (x - 34, y - 17, 68, 41))
        for side in (-1, 1):
            pygame.draw.polygon(s, CREAM, [(x + side * 22 - 8, y - 12), (x + side * 22 + 8, y - 12), (x + side * 22, y + 16)])

    def pip_wing(side):
        def paint(s, x, y):
            root = (x, y)
            tip = (x + side * 185, y - 65)
            lower = (x + side * 138, y + 152)
            pygame.draw.polygon(s, INK, [root, tip, (x + side * 166, y + 32), lower, (x + side * 63, y + 94)])
            pygame.draw.polygon(s, (75, 53, 72), [root, (tip[0] - side * 11, tip[1] + 12), (lower[0] - side * 12, lower[1] - 10), (x + side * 57, y + 79)])
            pygame.draw.line(s, (126, 82, 103), root, tip, 7)
        return paint

    def pip_feet(s, x, y):
        for side in (-1, 1):
            pygame.draw.line(s, INK, (x + side * 48, y), (x + side * 78, y + 39), 15)

    def pip_tongue(s, x, y):
        pygame.draw.line(s, INK, (x, y), (x + 430, y), 28)
        pygame.draw.line(s, (222, 86, 130), (x, y), (x + 430, y), 18)
        pygame.draw.circle(s, (222, 86, 130), (x + 430, y), 14)

    part("pipistrello", "body", pip_body, 1024)
    part("pipistrello", "wing_left", pip_wing(-1), 1024)
    part("pipistrello", "wing_right", pip_wing(1), 1024)
    part("pipistrello", "feet", pip_feet, 1024)
    part("pipistrello", "tongue", pip_tongue, 1024)

    def frog_body(s, x, y):
        points = [(x - 78, y), (x - 45, y - 38), (x + 45, y - 38), (x + 78, y), (x + 50, y + 38), (x - 50, y + 38)]
        pygame.draw.polygon(s, INK, points)
        pygame.draw.polygon(s, (78, 169, 77), [(x - 68, y), (x - 40, y - 31), (x + 40, y - 31), (x + 68, y), (x + 44, y + 31), (x - 44, y + 31)])
        pygame.draw.circle(s, INK, (x + 50, y - 20), 22)
        pygame.draw.circle(s, (108, 201, 91), (x + 50, y - 20), 16)
        pygame.draw.circle(s, CREAM, (x + 54, y - 22), 7)
        pygame.draw.circle(s, INK, (x + 56, y - 22), 3)
        pygame.draw.line(s, INK, (x + 35, y + 10), (x + 65, y + 14), 6)

    def frog_leg(s, x, y):
        pygame.draw.line(s, INK, (x, y), (x + 28, y + 28), 12)
        pygame.draw.line(s, (65, 142, 64), (x, y), (x + 28, y + 28), 6)

    part("frog_fish", "body", frog_body)
    part("frog_fish", "leg", frog_leg)

    def mother_body(s, x, y):
        pygame.draw.ellipse(s, INK, (x - 225, y - 185, 385, 280))
        pygame.draw.ellipse(s, (13, 16, 18), (x - 212, y - 173, 360, 255))

    def mother_head(defeated=False):
        def paint(s, x, y):
            pygame.draw.ellipse(s, INK, (x - 145, y - 145, 290, 300))
            pygame.draw.ellipse(s, (13, 16, 18), (x - 134, y - 134, 268, 278))
            for eye_x in (x - 47, x + 47):
                pygame.draw.circle(s, CREAM, (eye_x, y - 45), 25)
                if defeated:
                    pygame.draw.line(s, INK, (eye_x - 15, y - 60), (eye_x + 15, y - 30), 7)
                    pygame.draw.line(s, INK, (eye_x - 15, y - 30), (eye_x + 15, y - 60), 7)
                else:
                    pygame.draw.circle(s, INK, (eye_x + 6, y - 45), 9)
            pygame.draw.ellipse(s, (3, 5, 7), (x - 105, y + 13, 210, 96))
            for index in range(7):
                tooth_x = x - 86 + index * 29
                pygame.draw.polygon(s, CREAM, [(tooth_x - 12, y + 21), (tooth_x + 12, y + 21), (tooth_x, y + 56)])
                pygame.draw.polygon(s, CREAM, [(tooth_x - 12, y + 101), (tooth_x + 12, y + 101), (tooth_x, y + 66)])
        return paint

    def mother_hand(length, variation=0):
        def paint(s, x, y):
            target = x + length
            pygame.draw.line(s, INK, (x, y), (target, y + variation), 48)
            pygame.draw.line(s, (13, 16, 18), (x, y), (target, y + variation), 34)
            pygame.draw.circle(s, INK, (target, y + variation), 39)
            pygame.draw.circle(s, (13, 16, 18), (target, y + variation), 31)
        return paint

    part("troll_mother", "body", mother_body, 1024)
    part("troll_mother", "head", mother_head(False), 1024)
    part("troll_mother", "head_defeated", mother_head(True), 1024)
    part("troll_mother", "hand_1", mother_hand(205, 26), 1024)
    part("troll_mother", "hand_2", mother_hand(205, -18), 1024)
    part("troll_mother", "long_hand", mother_hand(440, 5), 1024)

    pygame.quit()
    print(f"Rig art complete: {written} PNG parts written, {kept} repainted parts preserved.")


if __name__ == "__main__":
    main()
