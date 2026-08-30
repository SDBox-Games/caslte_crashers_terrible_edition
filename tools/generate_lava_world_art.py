"""Generate editable Lava World PNG artwork with Pillow.

Run with:
    py games/castle_crashers_terrible_edition/tools/generate_lava_world_art.py

Every output is intentionally separate so it can be repainted without changing
runtime drawing code.
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "levels" / "lava_world"
SCALE = 2

INK = (29, 27, 33, 255)
CREAM = (247, 238, 210, 255)
GOLD = (247, 190, 56, 255)
ORANGE = (244, 87, 35, 255)
RED = (190, 43, 34, 255)


def font(size: int):
    for name in ("arialbd.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(name, size * SCALE)
        except OSError:
            continue
    return ImageFont.load_default()


class Art:
    def __init__(self, size: tuple[int, int], background=(0, 0, 0, 0)):
        self.size = size
        self.image = Image.new("RGBA", (size[0] * SCALE, size[1] * SCALE), background)
        self.draw = ImageDraw.Draw(self.image)

    @staticmethod
    def box(bounds):
        return tuple(int(value * SCALE) for value in bounds)

    @staticmethod
    def points(points):
        return [(int(x * SCALE), int(y * SCALE)) for x, y in points]

    def rect(self, bounds, fill, outline=None, width=1, radius=0):
        bounds = self.box(bounds)
        if radius:
            self.draw.rounded_rectangle(bounds, radius=radius * SCALE, fill=fill, outline=outline, width=width * SCALE)
        else:
            self.draw.rectangle(bounds, fill=fill, outline=outline, width=width * SCALE)

    def ellipse(self, bounds, fill, outline=None, width=1):
        self.draw.ellipse(self.box(bounds), fill=fill, outline=outline, width=width * SCALE)

    def line(self, points, fill, width=1):
        self.draw.line(self.points(points), fill=fill, width=width * SCALE, joint="curve")

    def polygon(self, points, fill):
        self.draw.polygon(self.points(points), fill=fill)

    def arc(self, bounds, start, end, fill, width=1):
        self.draw.arc(self.box(bounds), start=start, end=end, fill=fill, width=width * SCALE)

    def text(self, center, value, size, fill):
        self.draw.text(
            (int(center[0] * SCALE), int(center[1] * SCALE)), value,
            font=font(size), fill=fill, anchor="mm", align="center",
        )

    def save(self, name: str):
        OUTPUT.mkdir(parents=True, exist_ok=True)
        result = self.image.resize(self.size, Image.Resampling.LANCZOS)
        result.save(OUTPUT / f"{name}.png")


def gradient(art: Art, top, bottom):
    for y in range(art.size[1] * SCALE):
        amount = y / max(1, art.size[1] * SCALE - 1)
        color = tuple(int(top[i] + (bottom[i] - top[i]) * amount) for i in range(3)) + (255,)
        art.draw.line((0, y, art.size[0] * SCALE, y), fill=color)


def make_backdrop():
    art = Art((1280, 720), (27, 14, 24, 255))
    gradient(art, (27, 14, 24), (176, 51, 24))
    art.ellipse((1012, 24, 1148, 160), (243, 91, 27, 255))
    for base, color, spacing, heights in (
        (355, (54, 31, 39, 255), 205, (105, 160, 125, 220)),
        (405, (74, 37, 38, 255), 230, (130, 205, 155, 235)),
        (455, (107, 45, 34, 255), 270, (145, 225, 170, 255)),
    ):
        points = [(-100, 720)]
        for index in range(7):
            x = index * spacing - 80
            height = heights[index % len(heights)]
            points.extend(((x - spacing // 2, base), (x, base - height), (x + spacing // 2, base)))
        points.extend(((1380, 720),))
        art.polygon(points, color)
    art.rect((0, 420, 1280, 720), (167, 45, 19, 255))
    art.save("backdrop")


def make_wheel_chamber():
    art = Art((1280, 720), (18, 12, 20, 255))
    gradient(art, (18, 12, 20), (117, 35, 23))
    art.rect((0, 120, 1280, 595), (45, 39, 43, 255))
    for row in range(6):
        for column in range(12):
            x = column * 118 - (56 if row % 2 else 0)
            art.rect((x, 128 + row * 71, x + 108, 188 + row * 71), None, (76, 62, 59, 255), 4)
    art.rect((0, 525, 1280, 720), (29, 27, 31, 255))
    art.ellipse((710, 450, 1150, 670), INK)
    art.ellipse((725, 468, 1135, 650), ORANGE)
    art.save("wheel_chamber_background")


def make_cyclops_revival_area():
    art = Art((1280, 720), (13, 10, 17, 255))
    gradient(art, (13, 10, 17), (73, 25, 27))
    art.rect((0, 90, 1280, 560), (41, 35, 40, 255))
    for row in range(7):
        for column in range(11):
            x = column * 128 - (64 if row % 2 else 0)
            art.rect((x, 100 + row * 66, x + 118, 156 + row * 66), None, (82, 64, 60, 255), 4)
    art.rect((0, 520, 1280, 720), (25, 23, 28, 255))
    # Empty golden throne on the right.
    art.rect((923, 218, 1197, 584), INK, radius=26)
    art.rect((938, 233, 1182, 568), GOLD, radius=20)
    art.rect((967, 266, 1153, 550), (119, 48, 46, 255), radius=18)
    art.ellipse((914, 186, 980, 252), GOLD)
    art.ellipse((1140, 186, 1206, 252), GOLD)
    # Sealed lava pool where the Cyclops will rise.
    art.ellipse((675, 457, 1125, 689), INK)
    art.ellipse((693, 475, 1107, 668), (190, 52, 26, 255))
    for radius, color in ((92, (72, 21, 91, 255)), (58, (138, 48, 165, 255)), (21, CREAM)):
        art.ellipse((900 - radius, 565 - radius // 2, 900 + radius, 565 + radius // 2), color, width=1)
    art.save("cyclops_revival_background")


def make_wheel():
    art = Art((240, 240))
    art.ellipse((6, 6, 234, 234), INK)
    art.ellipse((22, 22, 218, 218), None, GOLD, 18)
    for angle in range(0, 360, 30):
        dx, dy = math.cos(math.radians(angle)) * 87, math.sin(math.radians(angle)) * 87
        art.line(((120, 120), (120 + dx, 120 + dy)), GOLD, 9)
    art.ellipse((95, 95, 145, 145), CREAM)
    art.save("golden_wheel")


def make_town_sign():
    art = Art((500, 340))
    art.line(((85, 340), (85, 55)), INK, 24)
    art.line(((85, 340), (85, 55)), (105, 70, 45, 255), 13)
    art.rect((10, 5, 490, 215), INK, radius=16)
    art.rect((22, 17, 478, 203), (226, 205, 157, 255), radius=12)
    art.text((250, 48), "VOLCANO TOWN!", 23, INK)
    art.text((250, 88), "NO ACTIVE VOLCANOS!", 18, RED)
    art.ellipse((144, 126, 168, 150), None, INK, 3)
    art.line(((156, 150), (156, 190)), INK, 4)
    art.line(((156, 159), (132, 176)), INK, 4)
    art.line(((156, 159), (181, 176)), INK, 4)
    art.polygon(((230, 193), (275, 135), (320, 193)), (91, 77, 67, 255))
    art.polygon(((249, 193), (275, 164), (301, 193)), ORANGE)
    art.line(((352, 165), (422, 165)), INK, 9)
    art.polygon(((442, 165), (412, 141), (412, 189)), INK)
    art.save("town_sign")


def make_town_house():
    art = Art((360, 310))
    art.rect((35, 105, 325, 310), INK, radius=24)
    art.rect((47, 117, 313, 298), (88, 72, 66, 255), radius=19)
    art.polygon(((10, 122), (180, 10), (350, 122)), INK)
    art.polygon(((30, 119), (180, 27), (330, 119)), (63, 53, 53, 255))
    art.ellipse((134, 181, 226, 307), (24, 21, 27, 255))
    art.line(((60, 152), (300, 152)), (116, 84, 70, 255), 7)
    art.save("town_house")


def make_statue():
    art = Art((150, 205))
    art.rect((15, 157, 135, 205), INK, radius=8)
    art.rect((23, 164, 127, 198), (77, 69, 65, 255), radius=6)
    art.ellipse((25, 24, 125, 136), INK)
    art.ellipse((34, 33, 116, 127), (116, 103, 92, 255))
    art.ellipse((52, 63, 66, 77), ORANGE)
    art.ellipse((84, 63, 98, 77), ORANGE)
    art.line(((32, 126), (7, 183)), INK, 17)
    art.line(((118, 126), (143, 183)), INK, 17)
    art.save("revival_statue")


def make_volcano():
    art = Art((440, 310))
    art.polygon(((8, 304), (68, 174), (143, 34), (279, 34), (358, 174), (423, 304)), INK)
    art.polygon(((24, 296), (82, 177), (150, 51), (272, 51), (345, 177), (407, 296)), (73, 58, 55, 255))
    art.ellipse((140, 7, 300, 81), INK)
    art.ellipse((151, 18, 289, 69), ORANGE)
    for eye_x in (162, 278):
        art.ellipse((eye_x - 24, 151, eye_x + 24, 185), INK)
        art.ellipse((eye_x - 16, 157, eye_x + 16, 179), GOLD)
    art.arc((156, 190, 284, 262), 0, 180, INK, 13)
    for index in range(5):
        lava_x = 138 + index * 41
        lava_h = 45 + (index * 37) % 75
        art.line(((lava_x, 59), (lava_x - 8, 59 + lava_h)), ORANGE, 13)
        art.line(((lava_x, 59), (lava_x - 8, 59 + lava_h)), GOLD, 5)
    art.save("volcano")


def make_fire_sign():
    art = Art((130, 230))
    art.line(((65, 230), (65, 60)), INK, 14)
    art.rect((7, 13, 123, 95), INK, radius=9)
    art.polygon(((65, 28), (39, 76), (91, 76)), RED)
    art.save("fire_sign")


def make_chest():
    art = Art((150, 105))
    art.rect((7, 22, 143, 105), INK, radius=12)
    art.rect((15, 30, 135, 97), (126, 78, 40, 255), radius=9)
    art.arc((27, 1, 123, 65), 180, 360, GOLD, 8)
    art.rect((65, 52, 85, 91), GOLD, radius=4)
    art.save("chest")


def make_sandwich_wall():
    art = Art((280, 390))
    art.ellipse((14, 54, 266, 376), INK)
    art.rect((14, 210, 266, 390), INK)
    art.ellipse((26, 66, 254, 361), (72, 77, 82, 255))
    art.rect((26, 215, 254, 378), (72, 77, 82, 255))
    for column in range(5):
        x = 57 + column * 42
        art.rect((x - 9, 101, x + 9, 364), INK, radius=5)
        art.rect((x - 4, 107, x + 4, 357), (157, 161, 157, 255), radius=3)
    art.ellipse((82, 190, 198, 306), INK)
    art.ellipse((91, 199, 189, 297), GOLD)
    # Readable sandwich emblem without depending on the item texture.
    art.polygon(((111, 231), (169, 231), (140, 204)), (234, 184, 75, 255))
    art.polygon(((111, 237), (169, 237), (140, 264)), (234, 184, 75, 255))
    art.line(((118, 235), (162, 235)), (71, 154, 66, 255), 8)
    art.text((140, 29), "SANDWICH REQUIRED", 16, CREAM)
    art.save("sandwich_wall")


def make_mountain(open_door: bool):
    art = Art((1450, 850))
    art.polygon(((5, 830), (475, 140), (855, 0), (1315, 830)), INK)
    art.polygon(((45, 820), (500, 175), (843, 42), (1275, 820)), (55, 48, 49, 255))
    entrance_fill = (18, 16, 21, 255) if open_door else (84, 68, 61, 255)
    art.ellipse((315, 500, 585, 850), INK)
    art.rect((315, 662, 585, 850), INK)
    art.ellipse((336, 523, 564, 841), entrance_fill)
    art.rect((336, 675, 564, 850), entrance_fill)
    art.save("dragon_mountain_open" if open_door else "dragon_mountain_closed")


def make_falling_sign():
    art = Art((300, 370))
    for x in (78, 222):
        art.line(((x, 370), (x, 172)), INK, 19)
        art.line(((x, 370), (x, 172)), (102, 67, 43, 255), 10)
    art.rect((28, 0, 272, 150), INK, radius=12)
    art.rect((39, 11, 261, 139), GOLD, radius=9)
    art.text((150, 48), "FALLING", 19, INK)
    art.text((150, 91), "ROCKS", 19, INK)
    art.ellipse((215, 78, 250, 113), (89, 72, 66, 255), INK, 5)
    art.save("falling_rocks_sign")


def make_dragon_head(dead=False):
    art = Art((500, 420))
    red = (112, 48, 43, 255) if dead else (178, 39, 32, 255)
    light = (133, 61, 52, 255) if dead else (225, 62, 42, 255)
    dark = (79, 39, 39, 255) if dead else (107, 24, 29, 255)
    x, y = 250, 350
    art.polygon(((108, 303), (45, 408), (455, 408), (392, 303)), INK)
    art.polygon(((120, 302), (66, 393), (434, 393), (380, 302)), dark)
    for side in (-1, 1):
        art.polygon(((x + side * 145, y - 157), (x + side * 238, y - 205), (x + side * 164, y - 91)), INK)
        art.polygon(((x + side * 151, y - 153), (x + side * 218, y - 190), (x + side * 163, y - 105)), (222, 176, 104, 255))
        art.polygon(((x + side * 91, y - 222), (x + side * 141, y - 340), (x + side * 51, y - 245)), INK)
        art.polygon(((x + side * 91, y - 232), (x + side * 131, y - 316), (x + side * 61, y - 245)), (232, 190, 118, 255))
    face = ((96, 246), (111, 137), (184, 80), (250, 103), (316, 80), (389, 137), (404, 246), (359, 315), (141, 315))
    art.polygon(face, INK)
    inner = tuple((int(px * .94 + x * .06), int(py * .94 + 210 * .06)) for px, py in face)
    art.polygon(inner, red)
    for side in (-1, 1):
        eye_x = x + side * 67
        art.polygon(((eye_x - 46, 164), (eye_x + 40, 143), (eye_x + 31, 211), (eye_x - 34, 215)), INK)
        if not dead:
            art.ellipse((eye_x - 29, 171, eye_x + 29, 209), GOLD)
            art.line(((eye_x, 175), (eye_x, 207)), INK, 8)
    art.ellipse((123, 223, 377, 328), INK)
    art.ellipse((135, 233, 365, 316), light)
    for nostril_x in (198, 302):
        art.ellipse((nostril_x - 14, 255, nostril_x + 14, 273), INK)
    art.ellipse((111, 281, 389, 405), INK)
    art.ellipse((124, 293, 376, 389), (35, 15, 21, 255))
    for tooth in range(7):
        tx = 149 + tooth * 34
        art.polygon(((tx, 299), (tx + 25, 299), (tx + 12, 340)), CREAM)
    art.arc((111, 314, 389, 418), 0, 180, light, 21)
    art.save("dragon_head_dead" if dead else "dragon_head")


def make_fist():
    art = Art((520, 320))
    red, light, shadow = (154, 35, 31, 255), (207, 55, 42, 255), (105, 25, 28, 255)
    x, y = 140, 200
    art.polygon(((x + 48, y - 30), (x + 290, y - 205), (x + 345, y - 105), (x + 98, y + 58)), INK)
    art.polygon(((x + 61, y - 22), (x + 286, y - 184), (x + 325, y - 111), (x + 91, y + 43)), red)
    art.ellipse((x - 116, y - 91, x + 116, y + 89), INK)
    art.ellipse((x - 104, y - 79, x + 104, y + 77), red)
    for index, knuckle_x in enumerate((-79, -29, 24, 75)):
        ky = y - (88 + (index in (1, 2)) * 8)
        art.ellipse((x + knuckle_x - 35, ky - 35, x + knuckle_x + 35, ky + 35), INK)
        art.ellipse((x + knuckle_x - 26, ky - 26, x + knuckle_x + 26, ky + 26), light)
        art.arc((x + knuckle_x - 18, ky - 13, x + knuckle_x + 18, ky + 16), 180, 360, shadow, 5)
    art.ellipse((x - 105, y - 19, x, y + 63), INK)
    art.ellipse((x - 93, y - 8, x - 11, y + 52), light)
    art.save("dragon_fist")


def make_boulder():
    art = Art((140, 140))
    art.ellipse((5, 5, 135, 135), INK)
    art.ellipse((12, 12, 128, 128), (91, 72, 65, 255))
    for x, y, radius in ((42, 44, 14), (91, 38, 11), (80, 93, 16)):
        art.ellipse((x - radius, y - radius, x + radius, y + radius), (55, 45, 44, 255))
    art.save("boulder")


def main():
    make_backdrop()
    make_wheel_chamber()
    make_cyclops_revival_area()
    make_wheel()
    make_town_sign()
    make_town_house()
    make_statue()
    make_volcano()
    make_fire_sign()
    make_chest()
    make_sandwich_wall()
    make_mountain(False)
    make_mountain(True)
    make_falling_sign()
    make_dragon_head(False)
    make_dragon_head(True)
    make_fist()
    make_boulder()
    print(f"Generated 18 editable Lava World PNGs in {OUTPUT}")


if __name__ == "__main__":
    main()
