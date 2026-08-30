"""Generate editable PNG art for Full Moon, Stovefaces, and Ice Thieves."""

from pathlib import Path
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
LEVEL = ROOT / "assets" / "levels" / "full_moon"
CHARS = ROOT / "assets" / "characters"
WEAPONS = ROOT / "assets" / "weapons"
INK = (25, 24, 23, 255)
BROWN = (104, 75, 57, 255)
BROWN_LIGHT = (151, 115, 82, 255)
STONE = (103, 84, 74, 255)
ICE = (133, 205, 229, 255)


def canvas(size):
    return Image.new("RGBA", size, (0, 0, 0, 0))


def save(folder, name, image):
    folder.mkdir(parents=True, exist_ok=True)
    image.save(folder / f"{name}.png")


def backdrop(name, icy=False):
    image = canvas((1280, 720)); d = ImageDraw.Draw(image)
    top = (20, 22, 31) if not icy else (37, 66, 91)
    bottom = (83, 67, 62) if not icy else (126, 177, 198)
    for y in range(720):
        t = y / 719
        d.line((0, y, 1280, y), fill=tuple(int(a + (b-a)*t) for a,b in zip(top,bottom)) + (255,))
    d.ellipse((965, 48, 1195, 278), fill=(231, 224, 194, 255), outline=INK, width=8)
    for x, y, r in ((1020, 105, 15), (1125, 92, 11), (1080, 180, 24), (1150, 215, 13), (1005, 225, 9)):
        d.ellipse((x-r, y-r, x+r, y+r), fill=(205, 198, 174, 255), outline=(183, 176, 155, 255), width=3)
    d.polygon([(0,430),(190,260),(365,390),(565,205),(770,385),(990,220),(1280,390),(1280,580),(0,580)], fill=(48,43,45,255))
    d.rectangle((0, 500, 1280, 720), fill=((116,101,87,255) if not icy else (167,211,226,255)))
    save(LEVEL, name, image)


def props():
    backdrop("path_backdrop"); backdrop("upper_backdrop"); backdrop("ice_backdrop", True)

    image=canvas((420,430)); d=ImageDraw.Draw(image)
    d.line((62,420,75,118),fill=INK,width=42); d.line((358,420,345,118),fill=INK,width=42)
    d.line((62,420,75,118),fill=(101,64,41,255),width=26); d.line((358,420,345,118),fill=(101,64,41,255),width=26)
    d.arc((68,25,352,250),180,360,fill=INK,width=48); d.arc((81,38,339,237),180,360,fill=(112,72,44,255),width=26)
    for x,y,a in ((55,210,-12),(355,260,15),(155,70,-18),(265,75,19)):
        d.line((x-25,y-10,x+25,y+10),fill=(171,111,61,255),width=8)
    save(LEVEL,"wooden_arch",image)

    image=canvas((420,210)); d=ImageDraw.Draw(image)
    for row in range(3):
        for col in range(5):
            x=8+col*84-(42 if row%2 else 0); y=8+row*68
            d.rounded_rectangle((x,y,x+98,y+64),12,fill=(119+row*5,91+col%2*6,75,255),outline=INK,width=5)
    save(LEVEL,"brown_stone",image)

    image=canvas((190,190)); d=ImageDraw.Draw(image)
    d.ellipse((12,18,178,180),fill=(93,83,79,255),outline=INK,width=10)
    for x,y,r in ((57,62,18),(124,47,13),(104,116,22),(48,130,12)):
        d.ellipse((x-r,y-r,x+r,y+r),fill=(68,62,61,255),outline=(130,116,104,255),width=4)
    save(LEVEL,"boulder",image)

    image=canvas((270,210)); d=ImageDraw.Draw(image)
    d.rectangle((25,92,245,205),fill=(111,69,43,255),outline=INK,width=9)
    d.polygon([(7,103),(135,15),(263,103)],fill=(92,56,38,255),outline=INK)
    d.rounded_rectangle((93,124,177,207),20,fill=(41,33,31,255),outline=INK,width=7)
    d.rectangle((45,120,88,160),fill=(183,139,81,255),outline=INK,width=5)
    save(LEVEL,"hut",image)

    image=canvas((115,560)); d=ImageDraw.Draw(image)
    d.line((24,5,24,555),fill=INK,width=18); d.line((91,5,91,555),fill=INK,width=18)
    d.line((24,5,24,555),fill=(125,79,45,255),width=9); d.line((91,5,91,555),fill=(125,79,45,255),width=9)
    for y in range(28,550,52):
        d.line((22,y,93,y),fill=INK,width=15); d.line((26,y,89,y),fill=(157,102,55,255),width=7)
    save(LEVEL,"ladder",image)

    for name,scale in (("mushroom",1),("super_mushroom",2)):
        image=canvas((150*scale,170*scale)); d=ImageDraw.Draw(image)
        d.rounded_rectangle((57*scale,65*scale,95*scale,165*scale),12*scale,fill=(218,192,145,255),outline=INK,width=6*scale)
        d.ellipse((8*scale,8*scale,142*scale,100*scale),fill=(158,63,49,255),outline=INK,width=8*scale)
        for x,y,r in ((44,42,12),(85,30,14),(112,59,10)):
            d.ellipse(((x-r)*scale,(y-r)*scale,(x+r)*scale,(y+r)*scale),fill=(239,220,175,255),outline=INK,width=3*scale)
        save(LEVEL,name,image)

    image=canvas((520,190)); d=ImageDraw.Draw(image)
    d.polygon([(5,180),(70,90),(145,126),(220,45),(310,115),(405,25),(515,180)],fill=(177,219,232,255),outline=INK)
    for x in (85,210,335,455):
        d.polygon([(x,165),(x+45,75),(x+85,168)],fill=(111,191,222,210),outline=(221,247,255,255))
    save(LEVEL,"ice_patch",image)

    image=canvas((320,310)); d=ImageDraw.Draw(image)
    d.polygon([(10,300),(80,145),(135,180),(190,55),(250,145),(310,300)],fill=(162,218,237,255),outline=INK)
    d.line((75,251,250,128),fill=(232,250,255,255),width=9)
    save(LEVEL,"ice_exit",image)


def character_parts(folder, armor, accent, stove=False, thief=False):
    target=CHARS/folder; target.mkdir(parents=True,exist_ok=True)
    for name in ("leg_left","leg_right"):
        image=canvas((64,105)); d=ImageDraw.Draw(image)
        d.rounded_rectangle((10,3,54,100),14,fill=armor,outline=INK,width=6); d.rectangle((7,76,58,102),fill=accent,outline=INK,width=5)
        image.save(target/f"{name}.png")
    for name in ("arm_left","arm_right"):
        image=canvas((62,104)); d=ImageDraw.Draw(image)
        d.rounded_rectangle((9,3,53,90),14,fill=armor,outline=INK,width=6); d.ellipse((11,74,52,103),fill=(186,139,92,255),outline=INK,width=5)
        image.save(target/f"{name}.png")
    image=canvas((120,140)); d=ImageDraw.Draw(image)
    d.rounded_rectangle((8,5,112,136),22,fill=armor,outline=INK,width=7)
    if stove:
        d.rectangle((29,31,91,112),fill=(48,48,49,255),outline=INK,width=6)
        for y in (52,72,92): d.line((36,y,84,y),fill=(117,120,117,255),width=5)
    else:
        d.polygon([(20,25),(100,25),(88,125),(32,125)],fill=accent,outline=INK)
    image.save(target/"body.png")
    image=canvas((156,140)); d=ImageDraw.Draw(image)
    if stove:
        d.rounded_rectangle((13,12,143,137),20,fill=(60,62,65,255),outline=INK,width=8)
        d.rectangle((28,36,128,103),fill=(37,38,40,255),outline=INK,width=6)
        for y in (52,72,91): d.line((36,y,120,y),fill=(122,125,122,255),width=6)
        d.ellipse((46,108,62,124),fill=(239,102,51,255),outline=INK,width=3); d.ellipse((94,108,110,124),fill=(239,102,51,255),outline=INK,width=3)
        d.rectangle((36,3,120,25),fill=(129,68,43,255),outline=INK,width=5)
    else:
        d.polygon([(18,18),(138,18),(130,135),(26,135)],fill=armor,outline=INK)
        d.line((30,38,126,55),fill=(210,238,247,255),width=8)
        d.ellipse((49,63,63,77),fill=INK); d.ellipse((94,63,108,77),fill=INK)
        if thief:
            for x,y in ((28,25),(118,35),(74,14)):
                d.line((x,y,x+15,y+24),fill=(228,246,255,255),width=4)
    image.save(target/"head.png")


def weapon():
    image=canvas((130,320)); d=ImageDraw.Draw(image)
    d.line((60,310,67,105),fill=INK,width=22); d.line((60,310,67,105),fill=(112,72,43,255),width=11)
    d.rounded_rectangle((20,18,115,125),24,fill=(65,67,70,255),outline=INK,width=9)
    d.rectangle((35,37,100,88),fill=(39,40,42,255),outline=INK,width=5)
    for y in (50,65,80): d.line((43,y,92,y),fill=(128,131,126,255),width=5)
    d.polygon([(19,53),(2,72),(22,88)],fill=(152,79,46,255),outline=INK)
    save(WEAPONS,"stoveface_mace",image)


def build():
    props(); weapon()
    character_parts("stoveface",(67,69,73,255),(151,80,48,255),stove=True)
    character_parts("ice_thief",(53,104,154,255),(172,220,239,255),thief=True)


if __name__ == "__main__":
    build()
