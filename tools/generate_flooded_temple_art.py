"""Generate editable PNG art for Flooded Temple, Fishman, Medusa, and the Horn."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageOps


ROOT = Path(__file__).resolve().parents[1]
LEVEL = ROOT / "assets" / "levels" / "flooded_temple"
CHARS = ROOT / "assets" / "characters"
BOSS = ROOT / "assets" / "bosses" / "medusa"
STONE_BOSS = ROOT / "assets" / "bosses" / "medusa_stone"
ITEMS = ROOT / "assets" / "items"
WEAPONS = ROOT / "assets" / "weapons"
INK = (24, 28, 25, 255)
STONE = (128, 139, 121, 255)
STONE_LIGHT = (171, 181, 157, 255)
GREEN = (51, 135, 83, 255)
WATER = (49, 148, 103, 255)
GOLD = (224, 174, 45, 255)


def canvas(size):
    return Image.new("RGBA", size, (0, 0, 0, 0))


def save(folder, name, image):
    folder.mkdir(parents=True, exist_ok=True)
    image.save(folder / f"{name}.png")


def gradient_backdrop(name, top, bottom, floor, water=False):
    image = canvas((1280, 720)); draw = ImageDraw.Draw(image)
    for y in range(720):
        amount = y / 719
        color = tuple(int(a + (b - a) * amount) for a, b in zip(top, bottom)) + (255,)
        draw.line((0, y, 1280, y), fill=color)
    draw.rectangle((0, 470, 1280, 720), fill=floor)
    if water:
        draw.rectangle((0, 515, 1280, 720), fill=(39, 125, 91, 255))
        for x in range(-50, 1350, 120):
            draw.arc((x, 500, x + 150, 548), 190, 350, fill=(106, 205, 140, 255), width=5)
    save(LEVEL, name, image)


def horn():
    """A bold curled war horn that remains readable in the small HUD circle."""
    image = canvas((240, 185)); draw = ImageDraw.Draw(image)
    # Dark outer silhouette, then layered brass body and bright inner rim.
    outer = [(20, 145), (54, 101), (85, 70), (122, 44), (180, 24), (222, 35),
             (198, 81), (165, 119), (119, 148), (68, 165)]
    draw.polygon(outer, fill=INK)
    inner = [(35, 142), (67, 107), (95, 82), (131, 61), (174, 44), (204, 46),
             (181, 74), (151, 103), (111, 128), (66, 148)]
    draw.polygon(inner, fill=(212, 150, 37, 255))
    draw.line(inner[:6], fill=(255, 224, 101, 255), width=10, joint="curve")
    # Flared bell with an inset opening and a leather grip.
    draw.ellipse((169, 12, 233, 80), fill=INK)
    draw.ellipse((178, 20, 224, 69), fill=(246, 193, 58, 255))
    draw.ellipse((189, 29, 220, 61), fill=(72, 50, 28, 255), outline=INK, width=4)
    draw.rounded_rectangle((66, 110, 107, 174), 10, fill=INK)
    draw.rounded_rectangle((73, 116, 100, 168), 7, fill=(103, 58, 34, 255))
    for y in (126, 142, 158):
        draw.line((75, y, 98, y - 5), fill=(224, 169, 77, 255), width=4)
    # Engraved bands help it read as a magical key rather than a food item.
    for start, stop in (((116, 52), (130, 130)), ((145, 39), (162, 109))):
        draw.line((start[0], start[1], stop[0], stop[1]), fill=INK, width=7)
        draw.line((start[0] + 5, start[1], stop[0] + 5, stop[1] - 3), fill=(253, 209, 78, 255), width=3)
    save(ITEMS, "horn", image)


def props():
    gradient_backdrop("approach_backdrop", (81, 151, 151), (174, 190, 132), (72, 139, 73, 255))
    gradient_backdrop("hall_backdrop", (31, 73, 68), (80, 121, 94), (91, 108, 91, 255), True)
    gradient_backdrop("lair_backdrop", (38, 66, 60), (99, 120, 84), (70, 126, 67, 255))

    image = canvas((760, 620)); d = ImageDraw.Draw(image)
    d.rectangle((30, 165, 730, 610), fill=(103, 115, 101, 255), outline=INK, width=12)
    for row in range(4):
        for col in range(7):
            x = 42 + col * 100 - (50 if row % 2 else 0); y = 177 + row * 105
            d.rounded_rectangle((x, y, x + 115, y + 94), 14, fill=STONE, outline=(83, 92, 80, 255), width=5)
    d.ellipse((190, 22, 570, 482), fill=INK)
    d.rectangle((190, 252, 570, 610), fill=INK)
    d.ellipse((228, 60, 532, 440), fill=(45, 53, 48, 255))
    d.rectangle((228, 250, 532, 610), fill=(45, 53, 48, 255))
    d.ellipse((290, 151, 470, 345), fill=(63, 72, 64, 255), outline=GOLD, width=12)
    save(LEVEL, "horn_wall_closed", image)

    opened = image.copy(); d = ImageDraw.Draw(opened)
    d.rectangle((212, 210, 548, 615), fill=(23, 34, 31, 255))
    d.ellipse((212, 43, 548, 430), fill=(23, 34, 31, 255), outline=(64, 75, 65, 255), width=8)
    save(LEVEL, "horn_wall_open", opened)

    image = canvas((420, 230)); d = ImageDraw.Draw(image)
    for index in range(6):
        x = index * 68; y = 175 - index * 27
        d.polygon([(x, 220), (x + 90, 220), (x + 90, y), (x + 25, y)], fill=STONE, outline=INK)
        d.line((x + 28, y + 8, x + 86, y + 8), fill=STONE_LIGHT, width=5)
    save(LEVEL, "stairs", image)

    image = canvas((500, 260)); d = ImageDraw.Draw(image)
    d.rectangle((12, 155, 488, 252), fill=(38, 122, 87, 255), outline=INK, width=8)
    for x in range(-30, 530, 95):
        d.arc((x, 118, x + 140, 195), 185, 350, fill=(123, 218, 151, 255), width=8)
    d.ellipse((55, 190, 180, 242), fill=(70, 163, 92, 255)); d.ellipse((315, 177, 454, 239), fill=(63, 151, 85, 255))
    save(LEVEL, "green_water", image)

    image = canvas((350, 570)); d = ImageDraw.Draw(image)
    d.rectangle((28, 135, 322, 558), fill=STONE, outline=INK, width=11)
    d.ellipse((28, 12, 322, 350), fill=STONE, outline=INK, width=11)
    d.ellipse((86, 74, 264, 343), fill=(31, 40, 37, 255), outline=INK, width=9)
    d.rectangle((86, 205, 264, 560), fill=(31, 40, 37, 255), outline=INK, width=9)
    for x, y in ((54,145),(296,145),(45,310),(304,310),(62,465),(286,465)):
        d.ellipse((x-30,y-30,x+30,y+30), fill=STONE_LIGHT, outline=INK, width=5)
    save(LEVEL, "temple_arch", image)

    image = canvas((230, 360)); d = ImageDraw.Draw(image)
    d.rounded_rectangle((42, 290, 188, 352), 18, fill=(91, 98, 88, 255), outline=INK, width=8)
    d.ellipse((66, 38, 164, 150), fill=STONE_LIGHT, outline=INK, width=8)
    d.rounded_rectangle((74, 125, 156, 285), 24, fill=STONE, outline=INK, width=8)
    d.line((80, 174, 34, 276), fill=INK, width=23); d.line((150, 174, 198, 276), fill=INK, width=23)
    d.line((100, 284, 83, 330), fill=INK, width=25); d.line((133, 284, 151, 330), fill=INK, width=25)
    d.ellipse((88, 72, 108, 95), fill=(203, 187, 68, 255)); d.ellipse((125, 72, 145, 95), fill=(203, 187, 68, 255))
    d.line((116, 96, 116, 135), fill=(89, 109, 77, 255), width=9)
    save(LEVEL, "snakey_statue", image)

    image = canvas((240, 370)); d = ImageDraw.Draw(image)
    d.rounded_rectangle((38, 300, 202, 362), 18, fill=(91, 98, 88, 255), outline=INK, width=8)
    d.ellipse((54, 30, 186, 163), fill=STONE_LIGHT, outline=INK, width=8)
    d.polygon([(54,75),(12,110),(54,132)], fill=STONE, outline=INK)
    d.ellipse((105, 76, 124, 96), fill=(78, 100, 77, 255), outline=INK, width=4)
    d.rounded_rectangle((72, 140, 166, 302), 25, fill=STONE, outline=INK, width=8)
    d.line((165, 154, 213, 335), fill=INK, width=14); d.line((169, 154, 217, 335), fill=(138, 117, 67, 255), width=7)
    save(LEVEL, "fishman_statue", image)

    image = canvas((620, 430)); d = ImageDraw.Draw(image)
    d.rounded_rectangle((18, 30, 602, 410), 40, fill=STONE, outline=INK, width=10)
    d.ellipse((68, 70, 255, 275), fill=(75, 133, 67, 255), outline=INK, width=8)
    d.ellipse((365, 70, 552, 275), fill=(48, 132, 105, 255), outline=INK, width=8)
    d.line((220, 235, 310, 175), fill=INK, width=24); d.line((400, 235, 310, 175), fill=INK, width=24)
    d.ellipse((281, 145, 339, 207), fill=GOLD, outline=INK, width=6)
    save(LEVEL, "handshake_statues", image)

    image = canvas((300, 560)); d = ImageDraw.Draw(image)
    d.rectangle((25, 0, 275, 560), fill=(55, 159, 112, 190), outline=INK, width=9)
    for y in range(20, 550, 65):
        d.arc((42, y, 258, y + 110), 5, 175, fill=(159, 232, 177, 230), width=7)
    save(LEVEL, "waterfall", image)

    image = canvas((250, 330)); d = ImageDraw.Draw(image)
    d.rounded_rectangle((22, 20, 228, 310), 18, fill=(93, 94, 82, 255), outline=INK, width=9)
    d.polygon([(38,40),(205,40),(178,138),(213,183),(145,300),(90,207),(39,254)], fill=(128, 199, 180, 255), outline=(225, 237, 217, 255))
    d.line((122,43,95,117,142,162,91,250), fill=INK, width=6)
    d.line((95,117,45,137), fill=INK, width=6); d.line((142,162,205,139), fill=INK, width=6)
    save(LEVEL, "broken_mirror", image)

    image = canvas((300, 340)); d = ImageDraw.Draw(image)
    d.rounded_rectangle((18,18,282,322),28,fill=(91,91,80,255),outline=INK,width=10)
    d.polygon([(35,42),(165,30),(118,142),(263,67),(199,193),(264,284),(137,247),(44,307),(82,178)], fill=(46,68,67,255), outline=(205,221,187,255))
    save(LEVEL, "broken_window", image)

    image = canvas((360, 150)); d = ImageDraw.Draw(image)
    d.ellipse((18,44,342,138), fill=(75, 119, 70, 255), outline=INK, width=9)
    for x in range(45, 330, 48):
        d.ellipse((x,20,x+53,87), fill=(73, 151, 76, 255), outline=INK, width=5)
    save(LEVEL, "snake_path", image)

    image = canvas((80, 80)); d = ImageDraw.Draw(image)
    d.ellipse((6,6,74,74), fill=(75, 191, 102, 190), outline=INK, width=6)
    d.ellipse((25,20,47,42), fill=(189, 244, 139, 220)); d.ellipse((49,45,63,59), fill=(160, 234, 119, 220))
    save(LEVEL, "poison_bubble", image)


def knight_parts(folder, armor, accent, fish=False, medusa=False):
    target = CHARS / folder; target.mkdir(parents=True, exist_ok=True)
    for name in ("leg_left", "leg_right"):
        image = canvas((74, 112)); d = ImageDraw.Draw(image)
        if medusa:
            d.polygon([(12,5),(62,5),(66,52),(43,106),(7,96),(30,55)], fill=armor, outline=INK)
            d.ellipse((15,69,70,108), fill=accent, outline=INK, width=6)
        else:
            d.rounded_rectangle((12,4,62,106),16,fill=armor,outline=INK,width=6); d.rectangle((8,78,67,108),fill=accent,outline=INK,width=5)
        image.save(target / f"{name}.png")
    for name in ("arm_left", "arm_right"):
        image = canvas((72, 112)); d = ImageDraw.Draw(image)
        d.rounded_rectangle((11,4,61,94),16,fill=armor,outline=INK,width=6); d.ellipse((13,78,61,109),fill=(185,139,93,255),outline=INK,width=5)
        image.save(target / f"{name}.png")
    image = canvas((128, 150)); d = ImageDraw.Draw(image)
    d.rounded_rectangle((8,6,120,146),25,fill=armor,outline=INK,width=8)
    if fish:
        d.polygon([(23,34),(105,34),(88,132),(40,132)],fill=accent,outline=INK); d.arc((37,72,92,127),10,170,fill=(232,236,174,255),width=7)
    elif medusa:
        d.polygon([(20,24),(108,24),(97,131),(31,131)],fill=accent,outline=INK); d.ellipse((48,52,80,84),fill=(80,153,68,255),outline=INK,width=5)
    image.save(target / "body.png")
    image = canvas((174, 155)); d = ImageDraw.Draw(image)
    if fish:
        d.ellipse((23,29,151,146),fill=armor,outline=INK,width=8); d.polygon([(24,72),(3,95),(28,114)],fill=accent,outline=INK)
        d.ellipse((89,55,121,86),fill=(241,230,105,255),outline=INK,width=5); d.ellipse((101,65,112,77),fill=INK)
        d.polygon([(141,87),(171,97),(141,107)],fill=accent,outline=INK); d.line((63,115,124,115),fill=INK,width=7)
    else:
        d.ellipse((27,33,147,148),fill=(189,139,91,255),outline=INK,width=8)
        for index, x in enumerate((20,45,70,100,127,150)):
            d.ellipse((x-20,2+(index%2)*12,x+25,72),fill=(57,137,62,255),outline=INK,width=6)
            d.ellipse((x-6,16+(index%2)*12,x+8,30+(index%2)*12),fill=(238,210,66,255),outline=INK,width=3)
        d.ellipse((59,70,78,91),fill=(244,220,80,255),outline=INK,width=3); d.ellipse((101,70,120,91),fill=(244,220,80,255),outline=INK,width=3)
        d.arc((66,88,113,125),5,175,fill=INK,width=6)
    image.save(target / "head.png")


def medusa_boss_parts():
    target = BOSS; target.mkdir(parents=True, exist_ok=True)
    # Copy-like but independently editable larger boss pieces.
    pieces = {
        "tail": ((300,300), [(20,35),(160,10),(270,70),(200,135),(278,205),(165,286),(35,245),(112,175)], (56,139,64,255)),
        "torso": ((220,270), [(28,250),(44,45),(176,45),(194,250)], (91,154,70,255)),
        "arm_left": ((100,245), [(35,12),(85,30),(62,225),(12,210)], (187,138,91,255)),
        "arm_right": ((100,245), [(15,30),(65,12),(88,210),(38,225)], (187,138,91,255)),
    }
    for name, (size, points, color) in pieces.items():
        image=canvas(size); d=ImageDraw.Draw(image); d.polygon(points,fill=color,outline=INK); save(target,name,image)
    image=canvas((280,230)); d=ImageDraw.Draw(image)
    d.ellipse((45,45,235,220),fill=(190,141,94,255),outline=INK,width=10)
    d.ellipse((88,105,120,139),fill=(250,224,72,255),outline=INK,width=4); d.ellipse((160,105,192,139),fill=(250,224,72,255),outline=INK,width=4)
    d.arc((103,145,181,195),10,170,fill=INK,width=9); save(target,"head",image)
    image=canvas((370,210)); d=ImageDraw.Draw(image)
    for index,x in enumerate(range(25,350,55)):
        y=25+(index%2)*18; d.ellipse((x-24,y,x+38,y+118),fill=(53,133,61,255),outline=INK,width=7)
        d.ellipse((x+5,y+25,x+20,y+41),fill=(248,218,70,255),outline=INK,width=3)
    save(target,"hair_snakes",image)
    image=canvas((110,115)); d=ImageDraw.Draw(image); d.polygon([(10,25),(88,10),(101,88),(35,108)],fill=(92,62,38,255),outline=INK); save(target,"boot",image)
    image=canvas((70,210)); d=ImageDraw.Draw(image); d.line((35,8,35,198),fill=INK,width=18); d.line((35,8,35,198),fill=(221,180,67,255),width=9)
    for y in range(18,130,24): d.line((10,y,60,y+8),fill=(88,139,70,255),width=9)
    save(target,"comb",image)
    image=canvas((430,420)); d=ImageDraw.Draw(image)
    d.polygon([(30,395),(55,155),(105,65),(215,22),(323,73),(385,178),(404,395)],fill=(143,147,133,255),outline=INK)
    d.line((130,87,288,331),fill=(101,104,95,255),width=8); d.line((300,92,154,350),fill=(101,104,95,255),width=8)
    save(target,"stone_shell",image)
    STONE_BOSS.mkdir(parents=True, exist_ok=True)
    for path in target.glob("*.png"):
        source = Image.open(path).convert("RGBA")
        gray = ImageOps.grayscale(source)
        tinted = ImageOps.colorize(gray, black=(62, 67, 62), white=(188, 194, 181)).convert("RGBA")
        tinted.putalpha(source.getchannel("A"))
        tinted.save(STONE_BOSS / path.name)


def spear():
    image=canvas((105,340)); d=ImageDraw.Draw(image)
    d.line((49,320,58,55),fill=INK,width=17); d.line((49,320,58,55),fill=(124,84,45,255),width=8)
    d.polygon([(59,5),(94,70),(61,58),(31,82)],fill=(187,198,169,255),outline=INK)
    d.line((28,182,81,184),fill=GOLD,width=12)
    save(WEAPONS,"fish_spear",image)


def build():
    horn(); props(); spear()
    knight_parts("fishman", (53,145,111,255), (188,221,101,255), fish=True)
    knight_parts("medusa", (66,142,68,255), (230,191,67,255), medusa=True)
    medusa_boss_parts()


if __name__ == "__main__":
    build()
