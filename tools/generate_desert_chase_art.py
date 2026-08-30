"""Generate editable PNG art for Desert Chase and the Sand Castle branch."""

from pathlib import Path
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
CHASE = ROOT / "assets" / "levels" / "desert_chase"
CASTLE = ROOT / "assets" / "levels" / "sand_castle"
CAMEL = ROOT / "assets" / "mounts" / "camel"
PETS = ROOT / "assets" / "pets"
SARACEN = ROOT / "assets" / "characters" / "saracen"
INK = (38, 30, 25, 255)
SAND = (224, 178, 91, 255)
SAND_LIGHT = (244, 207, 125, 255)


def canvas(size):
    return Image.new("RGBA", size, (0, 0, 0, 0))


def save(folder, name, image):
    folder.mkdir(parents=True, exist_ok=True)
    image.save(folder / f"{name}.png")


def rounded(draw, box, fill, radius=12, width=6, outline=INK):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def backdrop(folder, interior=False, roof=False):
    image = canvas((1280, 720)); draw = ImageDraw.Draw(image)
    if interior:
        draw.rectangle((0, 0, 1280, 720), fill=(173, 119, 63, 255))
        for row, y in enumerate(range(0, 720, 72)):
            for x in range(-80 + (row % 2) * 70, 1300, 140):
                draw.rounded_rectangle((x, y, x + 132, y + 65), 8, fill=(205, 157, 84, 255), outline=(111, 75, 43, 255), width=4)
        draw.rectangle((0, 510, 1280, 720), fill=(224, 183, 104, 255))
        for x in range(-80, 1350, 130):
            draw.line((x, 510, x + 120, 720), fill=(184, 137, 73, 255), width=4)
        save(folder, "interior_backdrop", image); return
    sky_top, sky_bottom = ((73, 146, 198), (221, 191, 129)) if not roof else ((71, 143, 199), (244, 214, 153))
    for y in range(720):
        amount = y / 720
        color = tuple(int(a + (b - a) * amount) for a, b in zip(sky_top, sky_bottom)) + (255,)
        draw.line((0, y, 1280, y), fill=color)
    draw.ellipse((1040, 62, 1170, 192), fill=(255, 234, 144, 255))
    draw.polygon([(0, 420), (250, 330), (510, 425), (790, 312), (1080, 418), (1280, 350), (1280, 535), (0, 535)], fill=(194, 143, 74, 255))
    draw.rectangle((0, 515, 1280, 720), fill=(228, 184, 98, 255) if not roof else (214, 160, 79, 255))
    save(folder, "roof_backdrop" if roof else "backdrop", image)


def chase_props():
    image = canvas((520, 310)); draw = ImageDraw.Draw(image)
    draw.ellipse((30, 120, 490, 285), fill=(54, 69, 72, 255), outline=INK, width=9)
    draw.pieslice((95, 25, 425, 245), 180, 360, fill=(113, 207, 147, 205), outline=INK, width=8)
    draw.rectangle((54, 205, 468, 257), fill=(74, 84, 85, 255), outline=INK, width=8)
    for x in (95, 180, 265, 350, 435):
        draw.ellipse((x-18, 216, x+18, 252), fill=(238, 197, 71, 255), outline=INK, width=4)
    draw.polygon([(34, 230), (3, 297), (132, 263)], fill=(54, 60, 62, 255), outline=INK)
    save(CHASE, "crashed_ufo", image)

    image = canvas((190, 220)); draw = ImageDraw.Draw(image)
    draw.ellipse((25, 30, 165, 205), fill=(75, 86, 90, 255), outline=INK, width=8)
    draw.ellipse((47, 55, 143, 150), fill=(100, 221, 153, 200), outline=INK, width=6)
    draw.rectangle((75, 178, 115, 218), fill=(99, 91, 67, 255), outline=INK, width=5)
    save(CHASE, "escape_pod", image)

    image = canvas((225, 120)); draw = ImageDraw.Draw(image)
    draw.ellipse((22, 52, 93, 112), fill=(228, 215, 50, 255), outline=INK, width=6)
    draw.ellipse((32, 63, 48, 81), fill=(22, 42, 27, 255)); draw.ellipse((61, 63, 77, 81), fill=(22, 42, 27, 255))
    draw.rounded_rectangle((88, 50, 185, 106), 18, fill=(75, 148, 70, 255), outline=INK, width=7)
    draw.line((112, 77, 205, 24), fill=INK, width=14); draw.line((119, 75, 201, 29), fill=(95, 171, 82, 255), width=7)
    save(CHASE, "dead_alien", image)

    image = canvas((360, 130)); draw = ImageDraw.Draw(image)
    for index in range(8):
        draw.ellipse((20 + index*13, 24 + index*4, 340-index*13, 115-index*3), outline=(132+index*5, 90+index*3, 43, 255), width=7)
    save(CHASE, "empty_sinkhole", image)

    image = canvas((780, 510)); draw = ImageDraw.Draw(image)
    draw.rectangle((90, 175, 690, 500), fill=SAND, outline=INK, width=10)
    for x in range(100, 690, 100):
        draw.line((x, 175, x, 500), fill=(182, 128, 65, 255), width=4)
    for y in range(245, 500, 75):
        draw.line((90, y, 690, y), fill=(182, 128, 65, 255), width=4)
    for x in (105, 225, 345, 465, 585):
        draw.rectangle((x, 105, x+82, 192), fill=SAND_LIGHT, outline=INK, width=7)
    draw.rounded_rectangle((292, 260, 488, 505), 86, fill=(72, 51, 38, 255), outline=INK, width=9)
    draw.ellipse((322, 295, 458, 430), fill=(32, 29, 29, 255))
    save(CHASE, "sand_castle", image)

    image = canvas((280, 500)); draw = ImageDraw.Draw(image)
    draw.rectangle((43, 118, 237, 492), fill=SAND, outline=INK, width=9)
    for x in (48, 110, 172): draw.rectangle((x, 48, x+60, 137), fill=SAND_LIGHT, outline=INK, width=7)
    draw.ellipse((87, 250, 193, 410), fill=(64, 45, 35, 255), outline=INK, width=8)
    save(CHASE, "sand_tower", image)

    image = canvas((70, 54)); draw = ImageDraw.Draw(image)
    draw.ellipse((4, 9, 65, 49), fill=(186, 223, 106, 255), outline=(45, 94, 45, 255), width=5)
    draw.ellipse((17, 4, 48, 30), fill=(224, 246, 147, 255))
    save(CHASE, "camel_spit", image)


def castle_props():
    image = canvas((240, 290)); draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((24, 18, 216, 280), 22, fill=(117, 74, 48, 255), outline=INK, width=8)
    draw.rounded_rectangle((48, 42, 192, 250), 18, fill=(95, 165, 202, 255), outline=(236, 212, 139, 255), width=10)
    draw.line((62, 54, 180, 238), fill=(238, 225, 182, 255), width=7)
    save(CASTLE, "window", image)
    draw.line((44, 65, 197, 225), fill=(90, 50, 39, 255), width=12)
    draw.line((188, 53, 65, 247), fill=(90, 50, 39, 255), width=10)
    save(CASTLE, "tiger_window", image)

    image = canvas((520, 420)); draw = ImageDraw.Draw(image)
    for index in range(9):
        y = 365 - index * 34; left = 38 + index * 22
        draw.polygon([(left, y), (500-left, y), (480-left, y+40), (left-20, y+40)], fill=(212, 163, 86, 255), outline=INK)
    draw.rounded_rectangle((345, 35, 500, 375), 65, fill=(73, 49, 39, 255), outline=INK, width=9)
    save(CASTLE, "staircase", image)

    for name, foreground in (("tower_back", False), ("tower_front", True)):
        image = canvas((285, 430)); draw = ImageDraw.Draw(image)
        color = SAND if foreground else (195, 147, 78, 230)
        draw.rectangle((44, 95, 241, 425), fill=color, outline=INK, width=8)
        for x in (45, 105, 165): draw.rectangle((x, 35, x+58, 115), fill=SAND_LIGHT if foreground else color, outline=INK, width=7)
        draw.ellipse((86, 205, 199, 375), fill=(73, 49, 39, 255), outline=INK, width=7)
        save(CASTLE, name, image)

    image = canvas((760, 260)); draw = ImageDraw.Draw(image)
    draw.polygon([(20, 225), (650, 25), (740, 225)], fill=(229, 183, 98, 255), outline=INK)
    for step in range(8):
        x = 65 + step * 75; y = 210 - step * 23
        draw.line((x, y, x+155, y), fill=(132, 88, 48, 255), width=6)
    save(CASTLE, "roof_ramp", image)

    image = canvas((180, 320)); draw = ImageDraw.Draw(image)
    draw.line((28, 12, 28, 310), fill=INK, width=13); draw.line((152, 12, 152, 310), fill=INK, width=13)
    draw.rectangle((31, 42, 149, 280), fill=(236, 225, 187, 110), outline=(242, 239, 218, 255), width=5)
    for x in range(38, 150, 22): draw.line((x, 44, x, 280), fill=(141, 124, 95, 255), width=2)
    for y in range(55, 280, 25): draw.line((32, y, 148, y), fill=(141, 124, 95, 255), width=2)
    save(CASTLE, "volleyball_net", image)
    image = canvas((82, 82)); draw = ImageDraw.Draw(image)
    draw.ellipse((4, 4, 78, 78), fill=(241, 224, 175, 255), outline=INK, width=6)
    draw.arc((8, 8, 74, 74), 40, 210, fill=(55, 147, 177, 255), width=10); draw.arc((8, 8, 74, 74), 220, 380, fill=(204, 78, 57, 255), width=10)
    save(CASTLE, "volleyball", image)
    image = canvas((270, 200)); draw = ImageDraw.Draw(image)
    draw.polygon([(20, 30), (240, 15), (250, 160), (135, 185), (25, 155)], fill=(229, 208, 147, 255), outline=INK)
    draw.line((135, 28, 135, 175), fill=(119, 91, 60, 255), width=5)
    draw.line((35, 75, 120, 110), fill=(51, 133, 161, 255), width=12); draw.line((148, 118, 232, 65), fill=(51, 133, 161, 255), width=12)
    draw.ellipse((105, 75, 165, 135), fill=(67, 163, 179, 255), outline=INK, width=5)
    save(CASTLE, "flooded_map", image)


def camel_parts():
    CAMEL.mkdir(parents=True, exist_ok=True)
    tan, light, dark = (191, 137, 74, 255), (229, 190, 126, 255), (87, 58, 39, 255)
    specs = {}
    image = canvas((260, 150)); draw = ImageDraw.Draw(image); draw.ellipse((20, 28, 240, 138), fill=tan, outline=INK, width=8); draw.ellipse((52, 2, 125, 82), fill=tan, outline=INK, width=7); draw.ellipse((120, 0, 191, 83), fill=tan, outline=INK, width=7); specs["body"] = image
    image = canvas((100, 190)); draw = ImageDraw.Draw(image); draw.polygon([(25,180),(72,180),(83,12),(48,2)], fill=tan, outline=INK); specs["neck"] = image
    image = canvas((150, 90)); draw = ImageDraw.Draw(image); draw.ellipse((8,18,142,82), fill=tan, outline=INK, width=7); draw.polygon([(34,25),(25,0),(57,20),(98,20),(117,0),(116,32)], fill=tan, outline=INK); draw.ellipse((103,37,115,49), fill=INK); specs["head"] = image
    image = canvas((115, 50)); draw = ImageDraw.Draw(image); draw.ellipse((5,3,110,45), fill=light, outline=INK, width=6); draw.line((74,25,100,25), fill=INK, width=3); specs["jaw"] = image
    for name in ("leg_back", "leg_front"):
        image = canvas((68, 130)); draw = ImageDraw.Draw(image); rounded(draw,(16,3,53,115),tan,16,7); draw.rounded_rectangle((8,99,60,126),10,fill=dark,outline=INK,width=6); specs[name]=image
    image = canvas((140, 76)); draw = ImageDraw.Draw(image); draw.arc((5,2,135,70),160,350,fill=INK,width=18); draw.arc((7,4,133,68),160,350,fill=dark,width=9); specs["tail"] = image
    image = canvas((150, 62)); draw = ImageDraw.Draw(image); rounded(draw,(7,7,143,55),(128,54,45,255),15,7); draw.line((34,14,42,52),fill=(239,191,68,255),width=6); draw.line((112,14,104,52),fill=(239,191,68,255),width=6); specs["saddle"] = image
    for name, image in specs.items(): image.save(CAMEL / f"{name}.png")


def pet_art():
    PETS.mkdir(parents=True, exist_ok=True)
    image = canvas((120, 100)); draw = ImageDraw.Draw(image)
    draw.ellipse((18,35,98,86), fill=(241,239,217,255), outline=INK, width=6)
    draw.ellipse((70,15,112,57), fill=(241,239,217,255), outline=INK, width=6)
    for x in (38,58,78): draw.polygon([(x,40),(x+12,40),(x+2,82),(x-10,82)], fill=(38,35,32,255))
    draw.line((25,65,8,45), fill=INK, width=7); draw.ellipse((93,27,101,35), fill=INK)
    save(PETS, "zebra", image)
    image = canvas((118, 104)); draw = ImageDraw.Draw(image)
    draw.ellipse((18,38,100,90), fill=(232,143,46,255), outline=INK, width=6)
    draw.ellipse((65,14,109,61), fill=(232,143,46,255), outline=INK, width=6)
    draw.polygon([(70,22),(74,2),(86,18),(98,17),(105,2),(108,28)], fill=(232,143,46,255), outline=INK)
    for x in (37,58,81): draw.line((x,42,x-10,80), fill=(75,45,27,255), width=7)
    draw.ellipse((92,30,100,38), fill=INK)
    save(PETS, "tiger", image)


def saracen_parts():
    SARACEN.mkdir(parents=True, exist_ok=True)
    white, green, skin = (228,229,209,255), (41,133,87,255), (169,103,65,255)
    for name in ("leg_left", "leg_right"):
        image=canvas((64,105)); draw=ImageDraw.Draw(image); rounded(draw,(10,3,54,98),white,15,6); draw.rounded_rectangle((6,75,59,103),10,fill=green,outline=INK,width=5); image.save(SARACEN/f"{name}.png")
    for name in ("arm_left", "arm_right"):
        image=canvas((62,104)); draw=ImageDraw.Draw(image); rounded(draw,(9,3,53,84),white,15,6); draw.ellipse((8,72,54,103),fill=skin,outline=INK,width=5); image.save(SARACEN/f"{name}.png")
    image=canvas((120,140)); draw=ImageDraw.Draw(image); rounded(draw,(8,5,112,134),white,22,7); draw.polygon([(18,30),(102,30),(91,125),(29,125)],fill=green,outline=INK); draw.polygon([(40,50),(80,50),(60,92)],fill=(240,195,69,255),outline=INK); image.save(SARACEN/"body.png")
    image=canvas((156,140)); draw=ImageDraw.Draw(image); rounded(draw,(13,26,143,136),white,24,8); draw.rectangle((25,15,131,54),fill=green,outline=INK,width=6); draw.polygon([(22,54),(134,54),(119,99),(37,99)],fill=(33,29,27,255)); draw.ellipse((48,67,67,85),fill=(237,196,126,255)); draw.ellipse((89,67,108,85),fill=(237,196,126,255)); draw.line((78,54,78,104),fill=(235,220,187,255),width=6); image.save(SARACEN/"head.png")


def build():
    backdrop(CHASE); backdrop(CASTLE, interior=True); backdrop(CASTLE, roof=True)
    chase_props(); castle_props(); camel_parts(); pet_art(); saracen_parts()


if __name__ == "__main__":
    build()
