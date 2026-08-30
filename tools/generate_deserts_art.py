"""Generate the editable, layered PNG art used by the Deserts level."""

from pathlib import Path
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
LEVEL = ROOT / "assets" / "levels" / "deserts"
CHARACTERS = ROOT / "assets" / "characters"
MAGIC = ROOT / "assets" / "magic" / "alien_hominid"
WEAPONS = ROOT / "assets" / "weapons"


def canvas(size):
    return Image.new("RGBA", size, (0, 0, 0, 0))


def save(name, image):
    LEVEL.mkdir(parents=True, exist_ok=True)
    image.save(LEVEL / f"{name}.png")


def outlined(draw, box, fill, radius=12, width=6, outline=(35, 27, 23, 255)):
    draw.rounded_rectangle(box, radius, fill=fill, outline=outline, width=width)


def character_parts(folder, armor, accent, alien=False):
    target = CHARACTERS / folder
    target.mkdir(parents=True, exist_ok=True)
    ink = (29, 28, 27, 255)
    for name in ("leg_left", "leg_right"):
        im = canvas((72, 108)); d = ImageDraw.Draw(im)
        outlined(d, (18, 5, 54, 96), armor, 16, 6, ink)
        d.rounded_rectangle((11, 78, 61, 103), 10, fill=accent, outline=ink, width=6)
        im.save(target / f"{name}.png")
    for name in ("arm_left", "arm_right"):
        im = canvas((76, 112)); d = ImageDraw.Draw(im)
        outlined(d, (18, 6, 58, 91), armor, 18, 6, ink)
        d.ellipse((15, 74, 61, 108), fill=accent, outline=ink, width=6)
        im.save(target / f"{name}.png")
    im = canvas((126, 130)); d = ImageDraw.Draw(im)
    outlined(d, (10, 7, 116, 123), armor, 26, 7, ink)
    d.polygon([(20, 32), (106, 32), (93, 113), (32, 113)], fill=accent, outline=ink)
    if alien:
        d.ellipse((43, 52, 83, 91), fill=(105, 214, 82, 255), outline=ink, width=5)
    else:
        d.line((29, 48, 97, 91), fill=(242, 205, 80, 255), width=10)
    im.save(target / "body.png")
    im = canvas((154, 152)); d = ImageDraw.Draw(im)
    if alien:
        d.ellipse((16, 16, 138, 139), fill=armor, outline=ink, width=8)
        d.ellipse((38, 50, 70, 83), fill=(17, 35, 25, 255), outline=ink, width=4)
        d.ellipse((84, 50, 116, 83), fill=(17, 35, 25, 255), outline=ink, width=4)
        d.arc((51, 72, 104, 119), 15, 165, fill=ink, width=6)
        d.ellipse((61, 3, 93, 37), fill=accent, outline=ink, width=5)
    else:
        outlined(d, (16, 23, 138, 140), armor, 25, 8, ink)
        d.polygon([(30, 65), (124, 65), (110, 97), (44, 97)], fill=(25, 23, 24, 255), outline=ink)
        d.ellipse((44, 73, 64, 91), fill=(235, 57, 47, 255))
        d.ellipse((90, 73, 110, 91), fill=(235, 57, 47, 255))
        d.rectangle((32, 15, 122, 45), fill=accent, outline=ink, width=6)
    im.save(target / "head.png")


def build():
    LEVEL.mkdir(parents=True, exist_ok=True)
    # Wide reusable desert sky and sand backdrop.
    im = canvas((1280, 720)); d = ImageDraw.Draw(im)
    for y in range(720):
        t = y / 720
        color = (int(84 + 121*t), int(155 + 65*t), int(205 - 60*t), 255) if y < 390 else (225, 183, 104, 255)
        d.line((0, y, 1280, y), fill=color)
    d.ellipse((1030, 70, 1160, 200), fill=(255, 235, 144, 255))
    d.polygon([(0, 390), (240, 315), (480, 390), (760, 292), (1040, 390), (1280, 325), (1280, 470), (0, 470)], fill=(188, 132, 71, 255))
    d.polygon([(0, 445), (250, 385), (550, 455), (875, 365), (1280, 440), (1280, 720), (0, 720)], fill=(225, 180, 96, 255))
    save("backdrop", im)

    im = canvas((460, 285)); d = ImageDraw.Draw(im)
    d.polygon([(25, 218), (95, 82), (385, 82), (445, 220)], fill=(91, 58, 38, 255), outline=(27, 27, 29, 255))
    d.rectangle((58, 118, 411, 235), fill=(105, 67, 43, 255), outline=(27, 27, 29, 255), width=8)
    d.polygon([(90, 116), (210, 35), (376, 116)], fill=(236, 228, 196, 255), outline=(27, 27, 29, 255))
    d.ellipse((155, 130, 300, 238), fill=(29, 43, 52, 255), outline=(27, 27, 29, 255), width=8)
    save("parked_ship", im)
    im = canvas((300, 230)); d = ImageDraw.Draw(im)
    d.polygon([(10, 210), (265, 15), (294, 48), (54, 224)], fill=(124, 78, 45, 255), outline=(38, 30, 25, 255))
    for i in range(7):
        x = 42 + i * 34; y = 184 - i * 25
        d.line((x, y, x + 76, y), fill=(230, 192, 117, 255), width=13)
    save("ship_stairs", im)

    im = canvas((150, 210)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((57, 45, 94, 205), 15, fill=(60, 132, 71, 255), outline=(34, 74, 42, 255), width=7)
    d.rounded_rectangle((17, 83, 67, 115), 14, fill=(60, 132, 71, 255), outline=(34, 74, 42, 255), width=7)
    d.rounded_rectangle((86, 112, 137, 145), 14, fill=(60, 132, 71, 255), outline=(34, 74, 42, 255), width=7)
    for x, y in ((74, 56), (73, 96), (78, 153), (40, 95), (115, 127)):
        d.line((x, y, x+8, y-9), fill=(239, 224, 168, 255), width=3)
    save("cactus", im)
    im = canvas((250, 145)); d = ImageDraw.Draw(im)
    d.rectangle((26, 66, 224, 135), fill=(209, 157, 75, 255), outline=(103, 72, 38, 255), width=7)
    for x in (48, 104, 160):
        d.rectangle((x, 28, x+40, 88), fill=(222, 173, 88, 255), outline=(103, 72, 38, 255), width=6)
    d.arc((85, 71, 165, 143), 180, 360, fill=(103, 72, 38, 255), width=7)
    save("sandcastle", im)

    im = canvas((350, 135)); d = ImageDraw.Draw(im)
    for i in range(9):
        box = (15+i*16, 40+i*3, 335-i*16, 118-i*2)
        d.ellipse(box, outline=(129+i*4, 88+i*3, 42, 245), width=8)
    save("sinkhole", im)
    im = canvas((310, 380)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((97, 105, 213, 372), 48, fill=(79, 157, 79, 255), outline=(29, 44, 30, 255), width=9)
    d.ellipse((52, 47, 258, 240), fill=(96, 182, 82, 255), outline=(29, 44, 30, 255), width=9)
    d.ellipse((80, 83, 231, 204), fill=(116, 120, 112, 255), outline=(32, 33, 31, 255), width=8)
    d.ellipse((108, 111, 203, 188), fill=(35, 28, 25, 255))
    for x in (101, 205): d.ellipse((x-18, 70, x+18, 106), fill=(224, 40, 38, 255), outline=(30, 22, 20, 255), width=5)
    save("antlion_body", im)
    for name, flip in (("antlion_claw_left", -1), ("antlion_claw_right", 1)):
        im = canvas((150, 180)); d = ImageDraw.Draw(im)
        d.arc((20, 18, 132, 150), 45 if flip > 0 else 135, 285 if flip > 0 else 395, fill=(125, 129, 121, 255), width=24)
        d.polygon([(75, 24), (125 if flip>0 else 25, 4), (112 if flip>0 else 38, 61)], fill=(171, 174, 166, 255), outline=(35,35,34,255))
        save(name, im)
    for name, fork in (("antlion_fork", True), ("antlion_knife", False)):
        im = canvas((80, 230)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((31, 65, 49, 224), 8, fill=(117, 73, 43, 255), outline=(36, 28, 24, 255), width=5)
        if fork:
            for x in (17, 32, 47, 62): d.line((x, 9, x, 78), fill=(188, 192, 188, 255), width=7)
            d.line((17, 69, 62, 69), fill=(188, 192, 188, 255), width=9)
        else:
            d.polygon([(15, 10), (65, 10), (51, 88), (29, 88)], fill=(196, 200, 197, 255), outline=(45,46,44,255))
        save(name, im)

    im = canvas((205, 120)); d = ImageDraw.Draw(im)
    d.ellipse((28, 32, 177, 106), fill=(78, 42, 23, 255), outline=(28,24,21,255), width=7)
    d.ellipse((72, 7, 135, 67), fill=(106, 57, 30, 255), outline=(28,24,21,255), width=6)
    for x1,y1,x2,y2 in ((46,79,5,106),(71,91,36,119),(137,91,171,119),(160,76,200,101)):
        d.line((x1,y1,x2,y2), fill=(44,30,22,255), width=10)
    d.ellipse((89, 29, 100, 40), fill=(241, 54, 43, 255)); d.ellipse((108, 29, 119, 40), fill=(241, 54, 43, 255))
    d.polygon([(78, 24), (51, 6), (88, 17)], fill=(56,35,24,255)); d.polygon([(127,24),(157,5),(118,17)], fill=(56,35,24,255))
    save("scorpion", im)

    # Scarab enemy animation parts.
    im = canvas((220, 220)); d = ImageDraw.Draw(im)
    d.ellipse((32, 24, 188, 207), fill=(23, 25, 27, 255), outline=(8, 10, 12, 255), width=9)
    d.polygon([(55, 87), (165, 87), (177, 178), (43, 178)], fill=(223, 172, 49, 255), outline=(37,31,20,255))
    d.ellipse((66, 49, 91, 73), fill=(230, 46, 44, 255)); d.ellipse((129,49,154,73), fill=(230,46,44,255))
    save("scarab_body", im)
    for name, facing in (("scarab_arm_left", -1), ("scarab_arm_right", 1)):
        im=canvas((130,180)); d=ImageDraw.Draw(im); d.line((65,40,65+facing*40,135), fill=(24,25,27,255), width=28); d.ellipse((24 if facing<0 else 76,124,62 if facing<0 else 114,166),fill=(30,31,33,255),outline=(8,9,10,255),width=6); save(name,im)
    for name, facing in (("scarab_wing_left", -1), ("scarab_wing_right", 1)):
        im=canvas((150,180)); d=ImageDraw.Draw(im); pts=[(75,28),(18 if facing<0 else 132,75),(37 if facing<0 else 113,163),(75,123)]; d.polygon(pts,fill=(66,73,73,235),outline=(17,19,20,255)); d.line((75,37,37 if facing<0 else 113,151),fill=(193,172,94,255),width=6); save(name,im)
    im=canvas((225,225)); d=ImageDraw.Draw(im); d.ellipse((14,14,211,211),fill=(22,24,26,255),outline=(7,8,9,255),width=10); d.arc((42,42,183,183),20,300,fill=(221,171,48,255),width=20); d.arc((66,66,159,159),190,510,fill=(147,106,34,255),width=13); save("scarab_ball",im)
    im=canvas((210,200)); d=ImageDraw.Draw(im); d.line((35,18,35,190),fill=(105,70,42,255),width=12); d.polygon([(39,22),(194,44),(166,116),(39,94)],fill=(242,240,221,255),outline=(50,48,44,255)); save("white_flag",im)

    # Alien craft parts and dropped masonry.
    im=canvas((500,240)); d=ImageDraw.Draw(im); d.ellipse((105,12,395,210),fill=(76,181,193,210),outline=(25,38,43,255),width=10); d.ellipse((20,102,480,230),fill=(95,101,106,255),outline=(27,30,32,255),width=10); d.ellipse((115,130,385,211),fill=(185,201,197,255),outline=(37,42,43,255),width=7); save("ufo_hull",im)
    im=canvas((230,160)); d=ImageDraw.Draw(im); d.ellipse((18,15,212,154),fill=(99,220,222,150),outline=(29,68,76,255),width=8); d.ellipse((62,74,168,143),fill=(216,230,70,255),outline=(41,49,27,255),width=6); save("ufo_dome",im)
    im=canvas((130,210)); d=ImageDraw.Draw(im); d.polygon([(38,12),(92,12),(119,191),(65,163),(11,191)],fill=(255,178,56,190)); d.polygon([(51,16),(79,16),(89,158),(65,137),(41,158)],fill=(238,245,202,230)); save("thruster_flame",im)
    im=canvas((250,205)); d=ImageDraw.Draw(im); outlined(d,(10,10,240,195),(174,139,92,255),9,9,(65,49,35,255)); d.line((18,62,232,62),fill=(88,64,43,255),width=8); d.line((18,129,232,129),fill=(88,64,43,255),width=8); d.line((85,15,85,190),fill=(88,64,43,255),width=7); d.line((169,15,169,190),fill=(88,64,43,255),width=7); save("alien_brick",im)
    im=canvas((1050,360)); d=ImageDraw.Draw(im); d.ellipse((85,20,965,330),fill=(53,61,67,255),outline=(15,18,21,255),width=14); d.ellipse((300,18,750,235),fill=(73,180,191,185),outline=(21,48,54,255),width=13); d.ellipse((180,208,870,348),fill=(145,158,157,255),outline=(27,31,32,255),width=12); [d.ellipse((x,250,x+48,298),fill=(118,255,132,255)) for x in range(240,820,95)]; save("mothership",im)
    im=canvas((520,620)); d=ImageDraw.Draw(im); d.polygon([(188,5),(332,5),(492,604),(28,604)],fill=(91,255,142,54),outline=(101,255,164,145)); [d.arc((65+i*22,65+i*35,455-i*22,580-i*14),0,360,fill=(138,255,177,120),width=5) for i in range(6)]; save("tractor_beam",im)
    im=canvas((260,180)); d=ImageDraw.Draw(im); [d.ellipse((24+i*22,45-(i%2)*20,115+i*22,140+(i%3)*10),fill=(105,102,92,110+i*10)) for i in range(6)]; save("smoke",im)
    im=canvas((260,260)); d=ImageDraw.Draw(im); d.polygon([(130,5),(159,79),(229,31),(192,105),(257,130),(185,151),(222,229),(153,188),(130,257),(102,189),(31,229),(72,153),(4,130),(78,105),(31,30),(103,79)],fill=(255,153,38,255),outline=(113,42,27,255)); d.ellipse((75,75,185,185),fill=(255,231,95,255)); save("explosion",im)
    for count in (1,2,3,5):
        im=canvas((330,220)); d=ImageDraw.Draw(im)
        for i in range(count):
            row=i//3; col=i%3; x=15+col*100+(row%2)*35; y=118-row*70
            outlined(d,(x,y,x+118,y+56),(196,156,91,255),8,6,(91,66,38,255)); d.line((x+12,y+18,x+105,y+18),fill=(226,190,125,255),width=5)
        save(f"brick_pile_{count}",im)

    character_parts("chain_guard", (89, 70, 49, 255), (223, 173, 60, 255))
    character_parts("scarab", (26, 27, 29, 255), (222, 171, 46, 255))
    character_parts("alien_hominid", (238, 221, 56, 255), (74, 151, 65, 255), alien=True)

    WEAPONS.mkdir(parents=True, exist_ok=True)
    im=canvas((120,310)); d=ImageDraw.Draw(im); d.line((61,45,61,280),fill=(104,70,43,255),width=18); [d.ellipse((50,55+i*22,72,77+i*22),fill=(80,84,82,255),outline=(28,29,28,255),width=3) for i in range(5)]; d.ellipse((18,8,104,94),fill=(70,73,72,255),outline=(22,24,23,255),width=8); [d.polygon([(61,2),(70+i*18,30),(52+i*12,40)],fill=(180,185,180,255)) for i in (-2,-1,0,1,2)]; im.save(WEAPONS/"chain_flail.png")
    im=canvas((125,330)); d=ImageDraw.Draw(im); d.rounded_rectangle((51,68,74,322),11,fill=(54,80,64,255),outline=(19,29,23,255),width=6); d.ellipse((10,4,115,112),fill=(82,224,103,255),outline=(21,62,31,255),width=8); d.ellipse((35,28,90,83),fill=(221,255,110,255),outline=(35,93,43,255),width=6); d.ellipse((48,43,77,72),fill=(248,255,201,255)); im.save(WEAPONS/"alien_staff.png")
    MAGIC.mkdir(parents=True, exist_ok=True)
    for name,size in (("projectile",96),("splash",190),("jump",150),("infusion",135)):
        im=canvas((size,size)); d=ImageDraw.Draw(im); d.ellipse((7,7,size-7,size-7),fill=(75,255,113,215),outline=(25,87,43,255),width=max(5,size//18)); d.ellipse((size*.3,size*.25,size*.7,size*.65),fill=(222,255,132,240)); im.save(MAGIC/f"{name}.png")


if __name__ == "__main__":
    build()
