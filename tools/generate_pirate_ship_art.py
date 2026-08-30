"""Generate editable PNG pieces for Pirate Ship and its Pirate enemy."""

from pathlib import Path
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
LEVEL = ROOT / "assets" / "levels" / "pirate_ship"
DESERT = ROOT / "assets" / "levels" / "deserts"
PIRATE = ROOT / "assets" / "characters" / "pirate"
INK = (12, 17, 22, 255)
WOOD = (116, 65, 35, 255)
WOOD_LIGHT = (171, 103, 53, 255)
GOLD = (235, 183, 61, 255)


def save(image, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def canvas(size):
    return Image.new("RGBA", size, (0, 0, 0, 0))


def outlined_polygon(draw, points, fill, width=10):
    draw.polygon(points, fill=fill)
    draw.line(points + [points[0]], fill=INK, width=width, joint="curve")


def make_backdrop():
    image = Image.new("RGB", (1280, 720), (83, 168, 205))
    draw = ImageDraw.Draw(image)
    for y in range(720):
        amount = y / 719
        color = (
            int(75 + 22 * amount), int(155 - 43 * amount), int(205 - 45 * amount)
        )
        draw.line((0, y, 1280, y), fill=color)
    draw.ellipse((930, 38, 1105, 213), fill=(255, 226, 138))
    for x in range(-40, 1320, 130):
        draw.arc((x, 298, x + 230, 410), 205, 335, fill=(220, 246, 245), width=8)
    save(image, LEVEL / "sea_backdrop.png")


def make_ship_parts():
    image = canvas((1280, 360)); draw = ImageDraw.Draw(image)
    outlined_polygon(draw, [(36, 70), (1240, 70), (1128, 285), (212, 330), (88, 240)], WOOD, 14)
    draw.rectangle((75, 61, 1195, 100), fill=INK)
    draw.rectangle((84, 70, 1184, 88), fill=WOOD_LIGHT)
    for x in range(125, 1160, 92):
        draw.line((x, 95, x + 58, 295), fill=(72, 40, 29), width=7)
    for x in range(160, 1140, 180):
        draw.ellipse((x, 160, x + 44, 205), fill=INK)
        draw.ellipse((x + 7, 167, x + 37, 198), fill=(44, 92, 111))
    save(image, LEVEL / "player_ship_hull.png")

    image = canvas((330, 280)); draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((15, 65, 315, 270), 18, fill=INK)
    draw.rounded_rectangle((28, 77, 302, 257), 14, fill=WOOD)
    draw.rectangle((0, 45, 330, 87), fill=INK)
    draw.rectangle((12, 54, 318, 75), fill=WOOD_LIGHT)
    draw.rounded_rectangle((108, 130, 220, 260), 9, fill=INK)
    draw.rounded_rectangle((119, 141, 209, 260), 7, fill=(38, 31, 30))
    save(image, LEVEL / "back_cabin.png")

    image = canvas((310, 250)); draw = ImageDraw.Draw(image)
    outlined_polygon(draw, [(22, 80), (288, 80), (265, 235), (50, 235)], WOOD, 12)
    draw.rectangle((4, 55, 306, 92), fill=INK)
    draw.rectangle((14, 64, 296, 80), fill=WOOD_LIGHT)
    save(image, LEVEL / "raised_deck.png")

    image = canvas((130, 650)); draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((39, 4, 91, 646), 22, fill=INK)
    draw.rounded_rectangle((50, 10, 80, 640), 14, fill=WOOD_LIGHT)
    save(image, LEVEL / "mast.png")

    image = canvas((510, 390)); draw = ImageDraw.Draw(image)
    outlined_polygon(draw, [(48, 32), (460, 65), (426, 350), (88, 326)], (239, 224, 184, 255), 13)
    for y in (115, 210, 300):
        draw.arc((35, y - 35, 470, y + 55), 5, 175, fill=(190, 166, 123), width=5)
    save(image, LEVEL / "sail.png")

    image = canvas((260, 120)); draw = ImageDraw.Draw(image)
    outlined_polygon(draw, [(18, 25), (242, 25), (210, 105), (48, 105)], WOOD, 11)
    draw.rectangle((12, 12, 248, 34), fill=INK)
    draw.rectangle((24, 18, 236, 26), fill=WOOD_LIGHT)
    save(image, LEVEL / "crow_nest.png")

    image = canvas((46, 560)); draw = ImageDraw.Draw(image)
    draw.line((23, 0, 23, 560), fill=INK, width=14)
    draw.line((23, 0, 23, 560), fill=(164, 117, 65), width=6)
    save(image, LEVEL / "rope.png")

    image = canvas((150, 170)); draw = ImageDraw.Draw(image)
    draw.ellipse((18, 5, 132, 165), fill=INK)
    draw.ellipse((29, 14, 121, 157), fill=WOOD)
    for y in (38, 83, 128):
        draw.rectangle((22, y, 128, y + 14), fill=INK)
        draw.rectangle((28, y + 4, 122, y + 10), fill=(92, 93, 88))
    draw.line((75, 15, 75, 157), fill=(73, 38, 27), width=6)
    save(image, LEVEL / "barrel.png")

    image = canvas((190, 75)); draw = ImageDraw.Draw(image)
    draw.line((16, 59, 149, 18), fill=INK, width=25)
    draw.line((16, 59, 149, 18), fill=GOLD, width=13)
    draw.ellipse((132, 5, 185, 45), fill=INK)
    draw.ellipse((141, 12, 177, 37), fill=(114, 173, 181), outline=GOLD, width=5)
    save(image, LEVEL / "spyglass.png")

    image = canvas((860, 350)); draw = ImageDraw.Draw(image)
    outlined_polygon(draw, [(20, 78), (840, 78), (765, 282), (160, 330), (60, 246)], (72, 43, 32, 255), 15)
    draw.rectangle((50, 68, 810, 108), fill=INK)
    draw.rectangle((62, 77, 798, 94), fill=(142, 79, 42))
    for x in range(145, 760, 140):
        draw.ellipse((x, 160, x + 39, 202), fill=INK)
        draw.ellipse((x + 7, 167, x + 32, 195), fill=(235, 181, 64))
    save(image, LEVEL / "enemy_ship_hull.png")

    image = canvas((520, 430)); draw = ImageDraw.Draw(image)
    outlined_polygon(draw, [(45, 25), (475, 57), (438, 395), (92, 355)], (45, 49, 55, 255), 14)
    draw.ellipse((176, 106, 348, 262), fill=(230, 221, 190), outline=INK, width=10)
    draw.ellipse((211, 141, 252, 184), fill=INK)
    draw.ellipse((282, 141, 323, 184), fill=INK)
    draw.polygon([(263, 178), (241, 215), (285, 215)], fill=INK)
    draw.line((190, 284, 332, 284), fill=(230, 221, 190), width=22)
    draw.line((204, 264, 204, 304), fill=INK, width=6)
    draw.line((318, 264, 318, 304), fill=INK, width=6)
    save(image, LEVEL / "pirate_sail.png")

    image = canvas((330, 110)); draw = ImageDraw.Draw(image)
    points = [(0, 58), (50, 25), (104, 62), (161, 19), (220, 64), (278, 24), (330, 58)]
    draw.line(points, fill=(225, 248, 250), width=22, joint="curve")
    draw.line(points, fill=(78, 173, 208), width=8, joint="curve")
    save(image, LEVEL / "wave.png")

    image = canvas((220, 220)); draw = ImageDraw.Draw(image)
    draw.polygon(
        [(110, 4), (137, 65), (201, 31), (169, 91), (218, 119),
         (156, 139), (179, 207), (119, 166), (85, 216), (75, 154),
         (8, 177), (53, 121), (3, 78), (72, 75)],
        fill=INK,
    )
    draw.polygon(
        [(110, 22), (134, 79), (181, 52), (156, 101), (199, 119),
         (144, 129), (158, 183), (116, 150), (88, 192), (87, 138),
         (31, 155), (70, 116), (31, 83), (81, 87)],
        fill=(255, 213, 78),
    )
    draw.ellipse((75, 75, 149, 149), fill=(255, 244, 181), outline=(255, 174, 54), width=10)
    save(image, LEVEL / "explosion.png")


def make_pirate():
    pieces = {}
    image = canvas((220, 220)); draw = ImageDraw.Draw(image)
    draw.ellipse((22, 18, 198, 202), fill=INK)
    draw.ellipse((37, 32, 183, 188), fill=(225, 183, 132))
    draw.polygon([(26, 64), (192, 64), (168, 18), (72, 14)], fill=(154, 37, 35), outline=INK)
    draw.ellipse((58, 91, 94, 126), fill=(242, 239, 215), outline=INK, width=7)
    draw.ellipse((122, 91, 158, 126), fill=(242, 239, 215), outline=INK, width=7)
    draw.ellipse((74, 102, 88, 116), fill=INK); draw.ellipse((128, 102, 142, 116), fill=INK)
    draw.arc((73, 121, 151, 176), 0, 180, fill=INK, width=8)
    pieces["head"] = image
    image = canvas((180, 230)); draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((20, 8, 160, 220), 28, fill=INK)
    draw.rounded_rectangle((33, 20, 147, 208), 22, fill=(49, 55, 62))
    draw.polygon([(90, 38), (116, 102), (90, 132), (63, 102)], fill=(231, 217, 185), outline=INK)
    draw.rectangle((30, 158, 150, 185), fill=(142, 39, 35), outline=INK, width=7)
    pieces["body"] = image
    for name, mirror in (("arm_left", False), ("arm_right", True)):
        image = canvas((105, 210)); draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((22, 8, 84, 176), 25, fill=INK)
        draw.rounded_rectangle((33, 20, 73, 166), 18, fill=(49, 55, 62))
        draw.ellipse((25, 153, 82, 208), fill=INK)
        draw.ellipse((35, 162, 72, 198), fill=(225, 183, 132))
        pieces[name] = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT) if mirror else image
    for name, mirror in (("leg_left", False), ("leg_right", True)):
        image = canvas((110, 190)); draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((24, 5, 83, 151), 22, fill=INK)
        draw.rounded_rectangle((35, 17, 72, 145), 16, fill=(74, 55, 48))
        draw.ellipse((10, 132, 99, 184), fill=INK)
        draw.ellipse((23, 141, 87, 172), fill=(42, 39, 38))
        pieces[name] = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT) if mirror else image
    for name, image in pieces.items():
        save(image, PIRATE / f"{name}.png")


def make_desert():
    image = Image.new("RGB", (1280, 720), (113, 179, 209)); draw = ImageDraw.Draw(image)
    draw.ellipse((1020, 45, 1165, 190), fill=(255, 224, 128))
    draw.polygon([(0, 410), (215, 325), (460, 405), (720, 300), (1010, 390), (1280, 320), (1280, 720), (0, 720)], fill=(221, 177, 91))
    draw.polygon([(0, 510), (250, 425), (585, 505), (880, 405), (1280, 480), (1280, 720), (0, 720)], fill=(238, 199, 113))
    save(image, DESERT / "backdrop.png")


if __name__ == "__main__":
    make_backdrop()
    make_ship_parts()
    make_pirate()
    make_desert()
    print("Generated Pirate Ship, Pirate, and Deserts PNG art.")
