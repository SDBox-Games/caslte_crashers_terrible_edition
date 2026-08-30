"""Generate editable PNG art for Industrial Castle and its character rigs.

Existing files are preserved unless ``--force`` is supplied, so repainted art
is never silently overwritten. Run from the SDBox root with::

    py games/castle_crashers_terrible_edition/tools/generate_industrial_castle_art.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw


GAME_DIR = Path(__file__).resolve().parents[1]
LEVEL_DIR = GAME_DIR / "assets" / "levels" / "industrial_castle"
RIG_DIR = GAME_DIR / "assets" / "art" / "rigs"
CHARACTER_DIR = GAME_DIR / "assets" / "characters"

INK = (8, 15, 24, 255)
STEEL = (77, 88, 101, 255)
LIGHT_STEEL = (151, 164, 169, 255)
DARK_STEEL = (38, 44, 54, 255)
GOLD = (242, 184, 62, 255)
RED = (190, 49, 49, 255)
BLUE = (75, 220, 255, 255)
GREEN = (75, 220, 117, 255)
CREAM = (248, 239, 213, 255)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="overwrite existing PNGs")
    args = parser.parse_args()
    written = kept = 0

    def save(path: Path, image: Image.Image) -> None:
        nonlocal written, kept
        if path.is_file() and not args.force:
            kept += 1
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        image.save(path)
        written += 1

    def transparent(size=(640, 640)):
        return Image.new("RGBA", size, (0, 0, 0, 0))

    def outline_rect(draw, box, fill, width=9, radius=8):
        draw.rounded_rectangle(box, radius=radius, fill=INK)
        inner = (box[0] + width, box[1] + width, box[2] - width, box[3] - width)
        draw.rounded_rectangle(inner, radius=max(2, radius - width // 2), fill=fill)

    def background(style: str):
        image = Image.new("RGBA", (1280, 720), DARK_STEEL)
        draw = ImageDraw.Draw(image)
        if style == "exterior":
            draw.rectangle((0, 0, 1280, 420), fill=(112, 154, 176, 255))
            draw.rectangle((0, 420, 1280, 720), fill=(66, 104, 66, 255))
            for y in range(95, 420, 58):
                for x in range(-55 if (y // 58) % 2 else 0, 1280, 118):
                    draw.rectangle((x, y, x + 108, y + 48), fill=(125, 100, 89, 255), outline=INK, width=4)
        elif style == "balcony":
            draw.rectangle((0, 0, 1280, 370), fill=(104, 159, 184, 255))
            draw.rectangle((0, 370, 1280, 720), fill=(61, 67, 76, 255))
            for x in range(0, 1280, 130):
                draw.line((x, 370, x + 65, 720), fill=(31, 36, 44, 255), width=7)
            draw.rectangle((0, 355, 1280, 380), fill=INK)
        else:
            top = (35, 42, 53, 255) if style != "boss" else (46, 26, 34, 255)
            image.paste(top, (0, 0, 1280, 720))
            for row, y in enumerate(range(80, 520, 62)):
                for x in range(-70 if row % 2 else 0, 1280, 142):
                    draw.rectangle((x, y, x + 132, y + 52), fill=(70, 78, 89, 255), outline=(27, 31, 39, 255), width=4)
            draw.rectangle((0, 520, 1280, 720), fill=(51, 56, 64, 255))
            for x in range(0, 1280, 120):
                draw.line((x, 520, x + 50, 720), fill=(30, 34, 42, 255), width=6)
        return image

    for name in ("exterior", "factory", "elevator", "upper", "boss", "balcony"):
        save(LEVEL_DIR / f"{name}_backdrop.png", background(name))

    def prop(name, painter, size=(640, 640)):
        image = transparent(size)
        painter(ImageDraw.Draw(image), image)
        save(LEVEL_DIR / f"{name}.png", image)

    def bush(draw, _):
        for cx, cy, r in ((230, 350, 95), (320, 295, 125), (420, 350, 100), (330, 405, 125)):
            draw.ellipse((cx-r, cy-r, cx+r, cy+r), fill=INK)
            draw.ellipse((cx-r+10, cy-r+10, cx+r-10, cy+r-10), fill=(58, 119, 66, 255))
    prop("bush", bush)

    def brick_wall(draw, _):
        draw.rectangle((25, 55, 615, 610), fill=INK)
        draw.rectangle((36, 66, 604, 599), fill=(118, 92, 86, 255))
        for row, y in enumerate(range(70, 600, 72)):
            for x in range(-30 if row % 2 else 35, 630, 130):
                draw.rectangle((x, y, x+120, y+62), outline=(63, 50, 51, 255), width=6)
    prop("brick_wall", brick_wall)

    def exterior_balcony(draw, _):
        # A long, unmistakable raised balcony that sits over the beefy door.
        draw.polygon(((95,350),(1505,350),(1570,420),(30,420)), fill=INK)
        draw.polygon(((125,360),(1475,360),(1515,400),(85,400)), fill=(105,112,121,255))
        draw.rectangle((72,192,1528,224), fill=INK)
        draw.rectangle((85,201,1515,215), fill=GOLD)
        for x in range(110, 1520, 92):
            draw.rectangle((x,205,x+22,362), fill=INK)
            draw.rectangle((x+6,214,x+16,352), fill=(133,142,151,255))
        for x in (180, 470, 1130, 1420):
            draw.polygon(((x,420),(x+105,420),(x+52,493)), fill=INK)
            draw.polygon(((x+18,420),(x+87,420),(x+52,468)), fill=(83,89,99,255))
        for x in range(155, 1470, 190):
            draw.ellipse((x,330,x+36,366), fill=GOLD, outline=INK, width=6)
    prop("exterior_balcony", exterior_balcony, (1600, 500))

    def dead_guard(draw, _):
        draw.ellipse((100, 420, 540, 510), fill=(5, 10, 15, 80))
        draw.rounded_rectangle((180, 320, 430, 455), radius=42, fill=INK)
        draw.rounded_rectangle((192, 331, 418, 443), radius=35, fill=(90, 111, 121, 255))
        draw.ellipse((390, 285, 510, 405), fill=INK)
        draw.ellipse((400, 295, 500, 395), fill=(105, 125, 134, 255))
        draw.line((175, 410, 100, 490), fill=INK, width=28)
        draw.line((420, 415, 525, 470), fill=INK, width=28)
        draw.line((430, 350, 476, 368), fill=CREAM, width=7)
        draw.line((430, 375, 476, 357), fill=CREAM, width=7)
    prop("dead_guard", dead_guard)

    for index, symbol in enumerate(("GEAR", "SWORD", "BOMB"), 1):
        def poster(draw, _, index=index, symbol=symbol):
            draw.polygon(((130,70),(510,86),(485,575),(155,555)), fill=INK)
            draw.polygon(((145,88),(493,101),(470,555),(170,538)), fill=(220,198,150,255))
            draw.rectangle((205,150,430,335), fill=(112,92,75,255), outline=INK, width=8)
            draw.ellipse((264,173,371,280), fill=(75,75,78,255), outline=INK, width=7)
            draw.text((232,365), "WANTED", fill=RED, stroke_width=2, stroke_fill=INK)
            draw.text((247,425), symbol, fill=INK)
            draw.text((263,485), f"#{index}", fill=INK)
        prop(f"bounty_poster_{index}", poster)

    def metal_plate(draw, _):
        draw.ellipse((95, 430, 545, 555), fill=INK)
        draw.ellipse((112, 444, 528, 540), fill=LIGHT_STEEL)
        for x in (155, 485):
            draw.ellipse((x-12, 475, x+12, 499), fill=DARK_STEEL)
    prop("metal_plate", metal_plate)

    def door(draw, _):
        draw.rounded_rectangle((120, 45, 520, 610), radius=120, fill=INK)
        draw.rounded_rectangle((137, 65, 503, 595), radius=105, fill=(69, 77, 87, 255))
        for x in range(180, 500, 62):
            draw.rounded_rectangle((x, 95, x+24, 572), radius=10, fill=LIGHT_STEEL, outline=INK, width=5)
        draw.ellipse((250, 250, 390, 390), fill=INK)
        draw.ellipse((266, 266, 374, 374), fill=GOLD)
        draw.polygon(((295,300),(345,300),(360,335),(320,365),(280,335)), fill=(120,70,38,255), outline=INK)
    prop("industrial_door", door)

    def sign(draw, _):
        outline_rect(draw, (95,210,545,400), RED, 12, 18)
        draw.text((210,270), "EXIT", fill=CREAM, stroke_width=3, stroke_fill=INK)
        draw.polygon(((190,305),(135,305),(165,275),(165,294)), fill=CREAM)
    prop("exit_sign", sign)

    def portrait(draw, _):
        outline_rect(draw, (110,70,530,580), GOLD, 16, 12)
        draw.rectangle((145,105,495,545), fill=(83,49,55,255), outline=INK, width=8)
        draw.ellipse((225,145,415,335), fill=(190,145,92,255), outline=INK, width=12)
        draw.ellipse((260,205,300,245), fill=CREAM, outline=INK, width=5)
        draw.ellipse((340,205,380,245), fill=CREAM, outline=INK, width=5)
        draw.polygon(((250,155),(320,75),(390,155)), fill=GOLD, outline=INK)
        draw.rectangle((230,340,410,520), fill=DARK_STEEL, outline=INK, width=10)
    prop("industrial_king_portrait", portrait)

    def tube_machine(draw, _):
        outline_rect(draw, (80,260,560,585), STEEL, 13, 22)
        for x in (195,445):
            draw.rounded_rectangle((x-72,75,x+72,420), radius=58, fill=INK)
            draw.rounded_rectangle((x-58,90,x+58,405), radius=45, fill=(75,190,194,180))
            draw.ellipse((x-36,120,x+36,192), fill=BLUE)
        for x in range(130,540,72):
            draw.ellipse((x,515,x+24,539), fill=DARK_STEEL)
    prop("tube_machine", tube_machine)

    def factory_diagram(draw, _):
        outline_rect(draw, (40,85,600,580), STEEL, 15, 12)
        draw.rectangle((90,135,550,510), fill=(221,209,169,255), outline=INK, width=7)
        draw.rectangle((135,300,310,440), fill=(91,96,102,255), outline=INK, width=7)
        draw.polygon(((150,300),(205,210),(255,300)), fill=(132,72,52,255), outline=INK)
        draw.line((310,370,490,370), fill=INK, width=8)
        for x in (350,395,440,485):
            draw.ellipse((x-18,325,x+18,361), fill=(93,105,119,255), outline=INK, width=4)
            draw.rectangle((x-16,360,x+16,430), fill=(183,54,63,255), outline=INK, width=4)
    prop("factory_diagram", factory_diagram)

    def poison_cannon(draw, _):
        draw.rounded_rectangle((190,285,420,535), radius=30, fill=INK)
        draw.rounded_rectangle((205,300,405,520), radius=23, fill=STEEL)
        draw.line((300,340,510,175), fill=INK, width=76)
        draw.line((300,340,510,175), fill=(98,112,124,255), width=57)
        draw.ellipse((465,128,575,238), fill=INK)
        draw.ellipse((480,143,560,223), fill=GREEN)
    prop("poison_cannon", poison_cannon)

    def poison_pool(draw, _):
        draw.rounded_rectangle((35,175,605,560), radius=95, fill=INK)
        draw.rounded_rectangle((50,190,590,545), radius=82, fill=(50,151,74,255))
        for x, y, radius in ((145,270,34),(250,440,24),(375,300,42),(505,455,31)):
            draw.ellipse((x-radius,y-radius,x+radius,y+radius), fill=(125,231,92,180), outline=(28,88,49,255), width=6)
    prop("poison_pool", poison_pool)

    def bridge(draw, _):
        outline_rect(draw, (30,230,610,465), LIGHT_STEEL, 11, 18)
        for x in range(75,600,88):
            draw.line((x,246,x+38,448), fill=(89,97,105,255), width=9)
        draw.line((45,345,595,345), fill=CREAM, width=5)
    prop("poison_bridge", bridge)

    def spike(draw, _):
        outline_rect(draw, (125,210,515,520), STEEL, 12, 16)
        for x in range(165,500,70):
            draw.polygon(((x,210),(x+30,115),(x+60,210)), fill=LIGHT_STEEL, outline=INK)
            draw.polygon(((x,520),(x+30,615),(x+60,520)), fill=LIGHT_STEEL, outline=INK)
    prop("spike_block", spike)

    def electric_post(draw, _):
        outline_rect(draw, (230,195,410,575), STEEL, 11, 20)
        draw.ellipse((195,90,445,340), fill=INK)
        draw.ellipse((216,111,424,319), fill=(53,107,150,255))
        draw.ellipse((248,143,392,287), fill=BLUE)
        for a, b in (((320,145),(270,80)),((365,205),(455,165)),((275,240),(190,285))):
            draw.line((*a,*b), fill=CREAM, width=11)
            draw.line((*a,*b), fill=BLUE, width=6)
    prop("electric_post", electric_post)

    def elevator(draw, _):
        outline_rect(draw, (50,360,590,570), STEEL, 13, 18)
        for x in range(85,570,85):
            draw.line((x,382,x+40,548), fill=DARK_STEEL, width=8)
        draw.rectangle((80,330,560,380), fill=GOLD, outline=INK, width=8)
    prop("elevator_platform", elevator)

    def sheets(draw, _):
        for index in range(5):
            y = 470-index*48
            draw.polygon(((115+index*15,y),(505-index*13,y-18),(535-index*13,y+58),(145+index*15,y+75)), fill=INK)
            draw.polygon(((126+index*15,y+9),(494-index*13,y-8),(521-index*13,y+48),(154+index*15,y+64)), fill=LIGHT_STEEL)
    prop("metal_sheets", sheets)

    def box(draw, _):
        outline_rect(draw, (155,235,485,555), (106,78,53,255), 12, 12)
        draw.line((170,250,470,540), fill=INK, width=18)
        draw.line((470,250,170,540), fill=INK, width=18)
        draw.rectangle((280,345,360,445), fill=GOLD, outline=INK, width=7)
    prop("food_box", box)

    for name, liquid in (("red", RED),("green", GREEN),("blue", BLUE)):
        def tank(draw, _, liquid=liquid):
            draw.rounded_rectangle((170,65,470,575), radius=90, fill=INK)
            draw.rounded_rectangle((188,84,452,556), radius=74, fill=(172,214,220,180))
            draw.rectangle((194,350,446,550), fill=liquid)
            draw.ellipse((245,175,395,325), fill=(*liquid[:3],120), outline=CREAM, width=6)
            draw.rectangle((145,535,495,600), fill=STEEL, outline=INK, width=9)
        prop(f"glass_tank_{name}", tank)

    def glass(draw, _):
        draw.rectangle((80,55,560,600), fill=(100,210,228,75), outline=INK, width=16)
        for x in (200,320,440):
            draw.line((x,70,x,585), fill=(210,245,249,120), width=5)
    prop("arena_glass", glass)

    def eye(draw, _):
        draw.polygon(((70,320),(180,205),(470,205),(570,320),(470,435),(180,435)), fill=INK)
        draw.polygon(((95,320),(195,230),(450,230),(545,320),(450,410),(195,410)), fill=RED)
        draw.ellipse((250,250,390,390), fill=CREAM)
        draw.ellipse((295,270,365,385), fill=INK)
    prop("angry_eye", eye)

    def turret(draw, _):
        outline_rect(draw, (120,245,430,555), STEEL, 13, 30)
        draw.ellipse((155,185,395,395), fill=INK)
        draw.ellipse((175,205,375,375), fill=(108,116,125,255))
        draw.line((335,300,555,170), fill=INK, width=75)
        draw.line((335,300,555,170), fill=LIGHT_STEEL, width=54)
        draw.ellipse((505,124,590,209), fill=INK)
        draw.ellipse((519,138,576,195), fill=RED)
    prop("boss_turret", turret)

    def pole(color):
        def paint(draw, _):
            draw.rounded_rectangle((250,120,390,585), radius=42, fill=INK)
            draw.rounded_rectangle((266,138,374,568), radius=31, fill=STEEL)
            draw.ellipse((190,65,450,325), fill=INK)
            draw.ellipse((213,88,427,302), fill=color)
            draw.ellipse((265,140,375,250), fill=CREAM)
        return paint
    prop("pole_blue", pole(BLUE))
    prop("pole_green", pole(GREEN))

    def pole_orb(color):
        def paint(draw, _):
            draw.ellipse((8,8,292,292), fill=INK)
            draw.ellipse((27,27,273,273), fill=color)
            draw.ellipse((83,64,217,198), fill=CREAM)
            draw.ellipse((106,87,194,175), fill=(255,255,255,220))
        return paint
    prop("pole_orb_blue", pole_orb(BLUE), (300, 300))
    prop("pole_orb_green", pole_orb(GREEN), (300, 300))

    def side_block(draw, _):
        outline_rect(draw, (115,115,525,555), (93,38,44,255), 14, 20)
        for y in range(175,520,95):
            draw.ellipse((225,y-42,415,y+42), fill=RED, outline=INK, width=8)
            draw.ellipse((280,y-25,360,y+25), fill=CREAM)
    prop("side_damage_block", side_block)

    def spyglass(draw, _):
        draw.line((130,460,420,245), fill=INK, width=92)
        draw.line((140,450,410,250), fill=GOLD, width=68)
        draw.line((170,425,230,380), fill=(179,116,33,255), width=32)
        draw.ellipse((345,150,570,365), fill=INK)
        draw.ellipse((365,170,550,345), fill=GOLD)
        draw.ellipse((400,205,515,315), fill=(103,214,235,255), outline=CREAM, width=9)
        draw.line((110,480,190,420), fill=(179,116,33,255), width=40)
    prop("golden_spyglass", spyglass, (640,640))

    def ice_view(draw, _):
        draw.rectangle((0,0,640,640), fill=(89,157,201,255))
        draw.polygon(((0,640),(0,390),(100,275),(170,390),(265,185),(360,395),(455,240),(545,400),(640,300),(640,640)), fill=(216,239,247,255), outline=INK)
        draw.rectangle((230,175,410,455), fill=(63,116,159,255), outline=INK, width=12)
        draw.polygon(((210,175),(320,65),(430,175)), fill=(187,226,241,255), outline=INK)
        draw.rectangle((275,245,365,390), fill=(28,45,72,255), outline=CREAM, width=7)
    prop("ice_castle_view", ice_view)

    def forest_pan(draw, _):
        draw.rectangle((0,0,640,640), fill=(105,174,199,255))
        draw.ellipse((470,65,590,185), fill=(255,225,142,255))
        for layer, color in enumerate(((45,99,64,255),(56,125,68,255),(73,150,75,255))):
            base = 280 + layer*85
            for x in range(-60-layer*35,700,115):
                draw.polygon(((x,base+180),(x+58,base-85),(x+116,base+180)), fill=INK)
                draw.polygon(((x+10,base+170),(x+58,base-68),(x+106,base+170)), fill=color)
        draw.rectangle((0,565,640,640), fill=(49,92,58,255))
    prop("forest_pan", forest_pan)

    def character_parts(folder: str, armor, accent, crown=False):
        sizes = {"head":(156,140),"body":(120,140),"arm_left":(62,104),"arm_right":(62,104),"leg_left":(64,105),"leg_right":(64,105)}
        for part_name, size in sizes.items():
            image = transparent(size)
            draw = ImageDraw.Draw(image)
            w, h = size
            if part_name == "head":
                draw.rounded_rectangle((5,14,w-6,h-5), radius=35, fill=INK)
                draw.rounded_rectangle((13,22,w-14,h-13), radius=29, fill=armor)
                draw.rectangle((25,64,w-26,94), fill=(29,35,45,255), outline=INK, width=5)
                draw.ellipse((43,70,61,88), fill=CREAM)
                draw.ellipse((w-62,70,w-44,88), fill=CREAM)
                if crown:
                    draw.polygon(((26,25),(47,1),(74,25),(104,1),(132,25)), fill=GOLD, outline=INK)
            elif part_name == "body":
                draw.rounded_rectangle((5,5,w-6,h-5), radius=25, fill=INK)
                draw.rounded_rectangle((14,14,w-15,h-14), radius=19, fill=armor)
                draw.polygon(((w//2,38),(w//2+24,72),(w//2,104),(w//2-24,72)), fill=accent, outline=INK)
            else:
                draw.rounded_rectangle((5,4,w-6,h-5), radius=22, fill=INK)
                draw.rounded_rectangle((12,11,w-13,h-12), radius=16, fill=armor)
                draw.rectangle((10,h-30,w-11,h-12), fill=accent)
            save(CHARACTER_DIR / folder / f"{part_name}.png", image)

    character_parts("fencer", (93,105,119,255), (183,54,63,255))
    character_parts("industrialist", (62,69,80,255), (224,147,44,255))
    character_parts("industrial_king", (58,65,77,255), (219,148,47,255), crown=True)

    # The frightened face is part of the character folder too, rather than
    # being hidden in a level-specific rig directory.
    king_big_head = transparent((156, 140))
    big_head_draw = ImageDraw.Draw(king_big_head)
    big_head_draw.rounded_rectangle((5,14,150,135), radius=35, fill=INK)
    big_head_draw.rounded_rectangle((13,22,142,127), radius=29, fill=(58,65,77,255))
    big_head_draw.rectangle((25,60,130,101), fill=(29,35,45,255), outline=INK, width=5)
    for x in (52, 104):
        big_head_draw.ellipse((x-23,62,x+23,108), fill=CREAM, outline=INK, width=5)
        big_head_draw.ellipse((x-5,77,x+7,93), fill=INK)
    big_head_draw.polygon(((26,25),(47,1),(74,25),(104,1),(132,25)), fill=GOLD, outline=INK)
    save(CHARACTER_DIR / "industrial_king" / "head_eyebig.png", king_big_head)

    def rig_part(rig: str, name: str, painter):
        image = transparent()
        painter(ImageDraw.Draw(image))
        save(RIG_DIR / rig / "parts" / f"{name}.png", image)

    def king_head(big=False):
        def paint(draw):
            draw.rounded_rectangle((245,230,395,380), radius=42, fill=INK)
            draw.rounded_rectangle((256,241,384,369), radius=34, fill=(190,145,92,255))
            eye_r = 25 if big else 12
            for x in (290,350):
                draw.ellipse((x-eye_r,285-eye_r,x+eye_r,285+eye_r), fill=CREAM, outline=INK, width=5)
                draw.ellipse((x-5,280,x+7,294), fill=INK)
            draw.polygon(((260,242),(287,200),(318,236),(351,196),(381,242)), fill=GOLD, outline=INK)
            draw.line((292,335,350,335), fill=INK, width=7)
        return paint

    def king_body(draw):
        draw.rounded_rectangle((260,245,380,405), radius=28, fill=INK)
        draw.rounded_rectangle((270,255,370,395), radius=22, fill=(58,65,77,255))
        draw.polygon(((320,270),(352,325),(320,380),(288,325)), fill=GOLD, outline=INK)
    def limb(vertical=True):
        def paint(draw):
            if vertical:
                draw.rounded_rectangle((295,248,345,392), radius=22, fill=INK)
                draw.rounded_rectangle((304,257,336,383), radius=15, fill=(58,65,77,255))
            else:
                draw.rounded_rectangle((275,265,365,375), radius=27, fill=INK)
                draw.rounded_rectangle((285,275,355,365), radius=21, fill=(58,65,77,255))
        return paint
    for name, painter in (("head",king_head()),("head_eyebig",king_head(True)),("body",king_body),("arm_left",limb()),("arm_right",limb()),("leg_left",limb()),("leg_right",limb())):
        rig_part("industrial_king", name, painter)

    def machine_arm(draw):
        draw.rounded_rectangle((70,285,560,355), radius=30, fill=INK)
        draw.rounded_rectangle((85,300,545,340), radius=20, fill=STEEL)
        for x in range(120,530,80):
            draw.ellipse((x,300,x+40,340), fill=LIGHT_STEEL, outline=INK, width=5)
    def machine_hand(draw):
        draw.rounded_rectangle((235,235,425,405), radius=54, fill=INK)
        draw.rounded_rectangle((250,250,410,390), radius=43, fill=(105,113,123,255))
        for index in range(4):
            x = 225 + index*58
            draw.rounded_rectangle((x,145,x+52,280), radius=22, fill=INK)
            draw.rounded_rectangle((x+8,154,x+44,270), radius=16, fill=LIGHT_STEEL)
    rig_part("industrial_hand", "arm", machine_arm)
    rig_part("industrial_hand", "hand", machine_hand)

    print(f"Industrial Castle art complete: {written} PNGs written, {kept} repainted PNGs preserved.")


if __name__ == "__main__":
    main()
