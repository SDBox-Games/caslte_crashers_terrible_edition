"""Generate editable PNG art for Wizard Castle Takeoff and the Painter."""

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
LEVEL = ROOT / "assets" / "levels" / "wizard_castle_takeoff"
CHARACTER = ROOT / "assets" / "characters" / "painter_boss"
WEAPONS = ROOT / "assets" / "weapons"
INK = (12, 16, 24, 255)
PURPLE = (141, 67, 190, 255)
PURPLE_LIGHT = (220, 137, 244, 255)
DIRT = (104, 74, 53, 255)
DIRT_LIGHT = (150, 107, 67, 255)
WOOD = (93, 58, 39, 255)
GREEN = (60, 211, 115, 255)
GREEN_LIGHT = (160, 255, 193, 255)


def canvas(size):
    return Image.new("RGBA", size, (0, 0, 0, 0))


def save(folder, name, image):
    folder.mkdir(parents=True, exist_ok=True)
    image.save(folder / f"{name}.png")


def gradient(size, top, bottom):
    image = canvas(size)
    draw = ImageDraw.Draw(image)
    for y in range(size[1]):
        mix = y / max(1, size[1] - 1)
        color = tuple(int(a + (b - a) * mix) for a, b in zip(top, bottom)) + (255,)
        draw.line((0, y, size[0], y), fill=color)
    return image


def backdrops():
    image = gradient((1280, 720), (30, 15, 52), (100, 54, 112))
    draw = ImageDraw.Draw(image)
    draw.ellipse((-180, 40, 430, 470), fill=(80, 47, 103, 255))
    draw.ellipse((810, 5, 1440, 485), fill=(66, 38, 91, 255))
    draw.polygon([(0, 515), (150, 492), (330, 525), (540, 485), (770, 520), (1000, 480), (1280, 520), (1280, 720), (0, 720)], fill=DIRT, outline=INK)
    draw.rectangle((0, 565, 1280, 720), fill=(119, 83, 56, 255))
    for x in range(20, 1280, 120):
        draw.line((x, 590 + x % 29, x + 65, 610 + x % 37), fill=(72, 50, 39, 255), width=5)
    save(LEVEL, "village_backdrop", image)

    image = gradient((1280, 720), (14, 7, 38), (102, 50, 140))
    draw = ImageDraw.Draw(image)
    draw.ellipse((100, 85, 480, 465), fill=(69, 34, 113, 180))
    draw.ellipse((780, 10, 1370, 590), fill=(92, 41, 136, 150))
    save(LEVEL, "flight_backdrop", image)

    image = gradient((1280, 720), (26, 13, 51), (111, 62, 121))
    draw = ImageDraw.Draw(image)
    draw.polygon([(0, 520), (160, 490), (350, 525), (600, 490), (850, 525), (1090, 485), (1280, 515), (1280, 720), (0, 720)], fill=DIRT, outline=INK)
    draw.rectangle((0, 565, 1280, 720), fill=(116, 82, 58, 255))
    save(LEVEL, "landing_backdrop", image)

    image = gradient((1280, 720), (13, 21, 30), (43, 74, 67))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 95, 1280, 720), fill=(42, 66, 65, 255), outline=INK, width=10)
    for y in range(120, 630, 95):
        for x in range(-40 + (y // 95 % 2) * 65, 1280, 130):
            draw.rounded_rectangle((x, y, x + 118, y + 82), 10, fill=(51, 84, 78, 255), outline=(29, 48, 49, 255), width=5)
    draw.rectangle((0, 555, 1280, 720), fill=(65, 74, 65, 255), outline=INK, width=9)
    save(LEVEL, "interior_backdrop", image)


def props():
    image = canvas((460, 390)); draw = ImageDraw.Draw(image)
    draw.polygon([(30, 365), (48, 150), (115, 85), (205, 125), (270, 42), (420, 128), (430, 365)], fill=WOOD, outline=INK)
    draw.polygon([(18, 155), (120, 42), (210, 78), (290, 12), (448, 145), (392, 168), (278, 80), (214, 145), (112, 112), (58, 180)], fill=(73, 43, 35, 255), outline=INK)
    draw.polygon([(84, 207), (165, 185), (170, 335), (78, 337)], fill=(32, 25, 27, 255), outline=INK)
    draw.polygon([(266, 185), (385, 197), (378, 288), (275, 278)], fill=(76, 42, 67, 255), outline=INK)
    draw.line((44, 220, 414, 105), fill=(156, 101, 59, 255), width=14)
    draw.line((220, 130, 236, 365), fill=INK, width=8)
    save(LEVEL, "broken_house", image)

    image = canvas((320, 250)); draw = ImageDraw.Draw(image)
    draw.ellipse((24, 68, 296, 228), fill=(45, 39, 45, 255), outline=INK, width=10)
    draw.ellipse((58, 88, 262, 188), fill=(15, 18, 29, 255), outline=(138, 91, 158, 255), width=7)
    draw.rectangle((50, 150, 270, 235), fill=(84, 58, 48, 255), outline=INK, width=8)
    draw.polygon([(38, 78), (80, 28), (245, 35), (286, 82)], fill=(111, 75, 55, 255), outline=INK)
    save(LEVEL, "broken_well", image)

    image = canvas((135, 250)); draw = ImageDraw.Draw(image)
    draw.polygon([(68, 5), (124, 102), (98, 225), (36, 242), (8, 115)], fill=PURPLE, outline=INK)
    draw.polygon([(68, 20), (82, 112), (60, 204), (35, 115)], fill=PURPLE_LIGHT)
    save(LEVEL, "purple_crystal", image)

    image = canvas((660, 560)); draw = ImageDraw.Draw(image)
    draw.polygon([(18, 520), (65, 190), (145, 102), (225, 145), (320, 20), (408, 142), (510, 82), (630, 202), (646, 520)], fill=(40, 181, 93, 255), outline=INK)
    draw.polygon([(80, 505), (122, 243), (220, 172), (315, 80), (405, 188), (536, 142), (590, 505)], fill=(91, 230, 135, 255), outline=INK)
    draw.ellipse((190, 245, 478, 635), fill=(17, 24, 34, 255), outline=INK, width=13)
    for x, y in ((92, 210), (202, 132), (400, 136), (550, 205)):
        draw.line((x, y, x + 45, y + 125), fill=GREEN_LIGHT, width=11)
    save(LEVEL, "green_crystal_cave", image)

    image = canvas((840, 330)); draw = ImageDraw.Draw(image)
    draw.polygon([(12, 30), (828, 30), (760, 120), (680, 132), (602, 254), (500, 212), (410, 322), (320, 220), (202, 270), (130, 134), (70, 118)], fill=(104, 73, 55, 255), outline=INK)
    for x, y in ((145, 125), (282, 210), (418, 250), (568, 185), (710, 95)):
        draw.polygon([(x, y), (x + 28, y + 78), (x - 22, y + 65)], fill=(65, 43, 40, 255), outline=INK)
    save(LEVEL, "floating_island_bottom", image)

    image = canvas((540, 560)); draw = ImageDraw.Draw(image)
    draw.polygon([(18, 535), (48, 175), (118, 75), (190, 128), (270, 12), (350, 125), (432, 72), (510, 180), (528, 535)], fill=(57, 167, 103, 255), outline=INK)
    draw.ellipse((115, 235, 430, 640), fill=(16, 25, 34, 255), outline=INK, width=13)
    draw.polygon([(270, 180), (202, 235), (235, 235), (235, 285), (305, 285), (305, 235), (338, 235)], fill=PURPLE_LIGHT, outline=INK)
    save(LEVEL, "castle_entrance", image)

    image = canvas((290, 390)); draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((22, 25, 268, 370), 34, fill=(56, 38, 55, 255), outline=INK, width=11)
    draw.polygon([(60, 54), (230, 54), (258, 164), (145, 205), (33, 164)], fill=(99, 61, 96, 255), outline=INK)
    draw.line((145, 72, 145, 332), fill=PURPLE_LIGHT, width=8)
    draw.ellipse((112, 240, 178, 307), fill=(175, 93, 188, 255), outline=INK, width=7)
    save(LEVEL, "giant_coffin", image)

    image = canvas((45, 45)); draw = ImageDraw.Draw(image)
    draw.ellipse((4, 4, 41, 41), fill=(192, 93, 233, 80))
    draw.ellipse((13, 13, 32, 32), fill=(236, 161, 255, 190))
    save(LEVEL, "purple_particle", image)

    debris = {
        "debris_plank": [(5, 24), (170, 5), (182, 39), (18, 59)],
        "debris_stone": [(8, 43), (42, 6), (105, 17), (128, 66), (91, 104), (28, 94)],
        "debris_roof": [(7, 92), (82, 8), (174, 88), (148, 120), (35, 119)],
        "debris_bone": [(13, 36), (38, 13), (63, 30), (132, 17), (153, 39), (128, 62), (59, 52), (34, 67)],
    }
    colors = {"debris_plank": WOOD, "debris_stone": (101, 94, 105, 255), "debris_roof": (83, 44, 61, 255), "debris_bone": (221, 213, 186, 255)}
    for name, points in debris.items():
        width = max(x for x, _ in points) + 8; height = max(y for _, y in points) + 8
        image = canvas((width, height)); draw = ImageDraw.Draw(image)
        draw.polygon(points, fill=colors[name], outline=INK)
        save(LEVEL, name, image)

    image = canvas((155, 155)); draw = ImageDraw.Draw(image)
    draw.ellipse((8, 8, 147, 147), fill=(75, 48, 43, 255), outline=INK, width=9)
    draw.ellipse((45, 45, 110, 110), fill=(22, 22, 29, 255), outline=INK, width=7)
    for angle in range(0, 360, 45):
        import math
        x = 77 + math.cos(math.radians(angle)) * 56
        y = 77 + math.sin(math.radians(angle)) * 56
        draw.line((77, 77, x, y), fill=(145, 89, 52, 255), width=7)
    save(LEVEL, "debris_wheel", image)


def painter():
    image = canvas((156, 140)); draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((12, 28, 144, 133), 16, fill=(87, 74, 75, 255), outline=INK, width=7)
    draw.rectangle((29, 52, 127, 119), fill=(214, 184, 154, 255), outline=INK, width=6)
    draw.arc((50, 75, 106, 111), 0, 180, fill=INK, width=5)
    draw.ellipse((48, 67, 60, 79), fill=INK); draw.ellipse((96, 67, 108, 79), fill=INK)
    draw.rounded_rectangle((25, 5, 131, 44), 8, fill=(76, 65, 67, 255), outline=INK, width=6)
    draw.arc((48, -13, 110, 31), 180, 360, fill=(190, 183, 166, 255), width=7)
    for x, color in ((38, (230, 64, 70, 255)), (62, (64, 148, 230, 255)), (87, (245, 198, 67, 255)), (111, (75, 202, 110, 255))):
        draw.ellipse((x - 7, 17, x + 7, 31), fill=color, outline=INK)
    save(CHARACTER, "head", image)

    image = canvas((120, 140)); draw = ImageDraw.Draw(image)
    draw.polygon([(22, 8), (98, 8), (112, 132), (8, 132)], fill=(87, 64, 66, 255), outline=INK)
    draw.polygon([(26, 25), (94, 25), (104, 129), (17, 129)], fill=(231, 225, 200, 255), outline=INK)
    for x, y, color in ((40, 65, (215, 67, 81, 255)), (70, 85, (67, 145, 226, 255)), (56, 112, (83, 194, 106, 255))):
        draw.ellipse((x - 9, y - 7, x + 9, y + 7), fill=color)
    save(CHARACTER, "body", image)

    for name, flip in (("arm_left", False), ("arm_right", True)):
        image = canvas((62, 104)); draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((13, 5, 50, 91), 16, fill=(91, 68, 68, 255), outline=INK, width=6)
        draw.ellipse((13, 74, 50, 102), fill=(214, 184, 154, 255), outline=INK, width=5)
        if flip:
            image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        save(CHARACTER, name, image)

    for name, flip in (("leg_left", False), ("leg_right", True)):
        image = canvas((64, 105)); draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((14, 4, 50, 90), 15, fill=(48, 43, 52, 255), outline=INK, width=6)
        draw.ellipse((8, 75, 55, 103), fill=(89, 60, 48, 255), outline=INK, width=5)
        if flip:
            image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        save(CHARACTER, name, image)

    image = canvas((105, 290)); draw = ImageDraw.Draw(image)
    draw.polygon([(46, 278), (60, 278), (72, 65), (39, 65)], fill=(141, 94, 53, 255), outline=INK)
    draw.polygon([(28, 72), (42, 9), (76, 9), (92, 72), (67, 105), (43, 105)], fill=(220, 211, 178, 255), outline=INK)
    draw.polygon([(34, 58), (48, 20), (60, 70), (72, 25), (84, 61), (67, 96), (43, 96)], fill=PURPLE, outline=INK)
    save(WEAPONS, "paintbrush", image)


def main():
    backdrops()
    props()
    painter()
    print("Generated Wizard Castle Takeoff, flight debris, Painter, coffin, and entrance PNGs.")


if __name__ == "__main__":
    main()
