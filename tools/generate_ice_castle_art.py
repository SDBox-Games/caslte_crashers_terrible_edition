"""Generate editable multipart Ice Castle, Ice King, weapon, and pet PNG art."""

from pathlib import Path
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
LEVEL = ROOT / "assets" / "levels" / "ice_castle"
CHARS = ROOT / "assets" / "characters" / "ice_king"
PETS = ROOT / "assets" / "pets"
WEAPONS = ROOT / "assets" / "weapons"
INK = (10, 19, 30, 255)
ICE = (124, 211, 241, 255)
ICE_LIGHT = (218, 249, 255, 255)
ICE_DARK = (52, 115, 157, 255)
STONE = (72, 119, 149, 255)
WOOD = (116, 72, 43, 255)


def canvas(size): return Image.new("RGBA", size, (0, 0, 0, 0))


def save(folder, name, image):
    folder.mkdir(parents=True, exist_ok=True)
    image.save(folder / f"{name}.png")


def room_backdrop(name, bridge=False, arena=False):
    image=canvas((1280,720)); d=ImageDraw.Draw(image)
    top=(16,42,70); bottom=(75,139,172)
    for y in range(720):
        t=y/719; d.line((0,y,1280,y),fill=tuple(int(a+(b-a)*t) for a,b in zip(top,bottom))+(255,))
    if bridge:
        d.polygon([(0,420),(230,180),(420,390),(640,120),(850,390),(1080,170),(1280,410),(1280,720),(0,720)],fill=(44,90,124,255))
        d.polygon([(0,490),(190,320),(390,480),(610,270),(810,485),(1030,300),(1280,470),(1280,720),(0,720)],fill=(95,163,193,255))
    else:
        d.rectangle((0,75,1280,720),fill=(70,124,155,255),outline=INK,width=10)
        for row in range(7):
            for col in range(13):
                x=col*112-(56 if row%2 else 0); y=84+row*72
                d.rounded_rectangle((x,y,x+104,y+64),10,fill=(82+row*3,145+col%2*6,177,255),outline=(43,94,128,255),width=5)
        for x in range(80,1280,210):
            d.polygon([(x,88),(x+35,205),(x+70,88)],fill=ICE_LIGHT,outline=ICE_DARK)
    floor=(188,229,240,255) if not arena else (148,207,225,255)
    d.rectangle((0,540,1280,720),fill=floor,outline=INK,width=10)
    d.polygon([(0,540),(95,502),(185,542),(310,505),(430,541),(550,500),(675,542),(790,507),(910,542),(1040,500),(1160,542),(1280,505),(1280,572),(0,572)],fill=ICE_LIGHT,outline=INK)
    save(LEVEL,name,image)


def environment():
    room_backdrop("hall_backdrop"); room_backdrop("upper_backdrop"); room_backdrop("bridge_backdrop",True); room_backdrop("arena_backdrop",arena=True)

    image=canvas((520,540)); d=ImageDraw.Draw(image)
    d.polygon([(18,520),(45,210),(105,95),(170,150),(235,35),(300,150),(375,85),(445,205),(500,520)],fill=ICE,outline=INK)
    d.ellipse((125,235,395,590),fill=(19,40,62,255),outline=INK,width=12)
    d.rectangle((125,395,395,540),fill=(19,40,62,255),outline=INK,width=12)
    for x,y in ((90,245),(180,145),(320,155),(430,255)):
        d.line((x,y,x-25,y+95),fill=ICE_LIGHT,width=11)
    save(LEVEL,"entrance_arch",image)

    image=canvas((120,260)); d=ImageDraw.Draw(image)
    d.rounded_rectangle((43,110,77,255),8,fill=(68,48,39,255),outline=INK,width=7)
    d.polygon([(60,5),(19,105),(60,86),(101,105)],fill=(245,99,47,255),outline=INK)
    d.polygon([(60,35),(39,93),(60,78),(81,93)],fill=(255,221,83,255))
    save(LEVEL,"torch",image)

    image=canvas((440,310)); d=ImageDraw.Draw(image)
    d.polygon([(18,292),(26,68),(92,18),(402,18),(423,292)],fill=(37,76,105,255),outline=INK)
    d.ellipse((245,70,392,245),fill=(24,41,56,255),outline=INK,width=9)
    d.ellipse((278,100,361,220),fill=(82,95,99,255),outline=INK,width=8)
    d.polygon([(320,85),(337,35),(354,86)],fill=(205,214,207,255),outline=INK)
    d.rounded_rectangle((75,106,180,220),20,fill=(63,82,96,255),outline=INK,width=9)
    d.ellipse((93,124,162,197),fill=(218,48,55,255),outline=INK,width=8)
    save(LEVEL,"button_nuke",image)

    image=canvas((300,250)); d=ImageDraw.Draw(image)
    d.rounded_rectangle((15,18,285,238),16,fill=(76,111,132,255),outline=INK,width=10)
    d.rectangle((35,48,265,211),fill=(34,59,77,255),outline=INK,width=7)
    d.line((150,28,150,230),fill=(119,173,196,255),width=9)
    for x in (85,215): d.ellipse((x-9,112,x+9,132),fill=(232,196,76,255),outline=INK,width=4)
    save(LEVEL,"cabinet",image)

    image=canvas((560,360)); d=ImageDraw.Draw(image)
    for step in range(6):
        x=20+step*72; y=300-step*47
        d.polygon([(x,y),(x+170,y),(x+210,y+48),(x+40,y+48)],fill=(123,197,220,255),outline=INK)
    save(LEVEL,"stairs",image)

    image=canvas((340,420)); d=ImageDraw.Draw(image)
    for i in range(7):
        x=15+(i%2)*15; y=18+i*55
        d.rounded_rectangle((x,y,325,y+48),8,fill=(116+i%2*11,72,43,255),outline=INK,width=7)
        d.ellipse((x+20,y+14,x+43,y+37),fill=(72,44,30,255))
    d.line((55,45,285,388),fill=(176,113,63,255),width=13); d.line((282,42,72,385),fill=(176,113,63,255),width=13)
    save(LEVEL,"wooden_wall",image)

    image=canvas((430,90)); d=ImageDraw.Draw(image)
    d.polygon([(7,57),(42,31),(116,19),(172,35),(241,17),(306,34),(386,23),(423,57)],fill=ICE,outline=INK)
    d.polygon([(7,57),(423,57),(390,84),(35,84)],fill=(63,145,184,255),outline=INK)
    for x in (95,205,330): d.line((x,31,x-18,56),fill=ICE_LIGHT,width=7)
    save(LEVEL,"bridge_segment",image)

    image=canvas((360,470)); d=ImageDraw.Draw(image)
    d.polygon([(18,450),(30,155),(85,70),(145,112),(180,18),(218,110),(284,65),(330,155),(344,450)],fill=ICE,outline=INK)
    d.ellipse((78,185,282,500),fill=(26,47,67,255),outline=INK,width=11)
    d.polygon([(180,230),(110,295),(145,295),(145,350),(215,350),(215,295),(250,295)],fill=(221,67,66,255),outline=INK)
    d.ellipse((125,145,155,180),fill=ICE_LIGHT,outline=INK,width=5); d.ellipse((205,145,235,180),fill=ICE_LIGHT,outline=INK,width=5)
    save(LEVEL,"angry_door",image)

    image=canvas((150,420)); d=ImageDraw.Draw(image)
    d.polygon([(75,4),(142,330),(105,405),(43,405),(8,330)],fill=ICE,outline=INK)
    d.line((74,42,98,330),fill=ICE_LIGHT,width=13)
    save(LEVEL,"ice_spike",image)

    image=canvas((360,190)); d=ImageDraw.Draw(image)
    d.polygon([(8,160),(55,65),(102,125),(155,18),(210,125),(267,52),(350,160)],fill=(146,226,248,210),outline=INK)
    for x,y in ((62,87),(162,48),(270,75)): d.line((x,y,x-20,145),fill=ICE_LIGHT,width=8)
    save(LEVEL,"ice_wave",image)

    image=canvas((190,240)); d=ImageDraw.Draw(image)
    d.rounded_rectangle((8,8,182,232),20,fill=(144,224,247,150),outline=(214,250,255,230),width=10)
    d.line((35,38,150,205),fill=(224,252,255,170),width=8); d.line((155,35,65,215),fill=(102,188,220,180),width=6)
    save(LEVEL,"ice_cube",image)

    image=canvas((260,210)); d=ImageDraw.Draw(image)
    d.rounded_rectangle((18,74,242,197),18,fill=(98,57,41,255),outline=INK,width=10)
    d.polygon([(20,82),(52,28),(208,28),(240,82)],fill=(131,76,44,255),outline=INK)
    d.rectangle((110,92,150,152),fill=(236,193,64,255),outline=INK,width=7)
    d.polygon([(130,6),(103,45),(120,45),(120,68),(140,68),(140,45),(157,45)],fill=(83,213,106,255),outline=INK)
    save(LEVEL,"ice_chest",image)

    image=canvas((350,420)); d=ImageDraw.Draw(image)
    d.polygon([(40,400),(58,95),(110,35),(175,90),(240,30),(292,100),(315,400)],fill=(82,166,202,255),outline=INK)
    d.rounded_rectangle((82,145,270,385),22,fill=(45,84,127,255),outline=INK,width=10)
    for x in (98,255): d.ellipse((x-25,80,x+25,130),fill=ICE_LIGHT,outline=INK,width=7)
    save(LEVEL,"ice_throne",image)


def character_and_items():
    def part(name,size,draw):
        image=canvas(size); draw(ImageDraw.Draw(image)); save(CHARS,name,image)
    part("head",(230,210),lambda d:(d.polygon([(30,165),(40,58),(80,42),(94,8),(115,45),(141,7),(154,46),(194,58),(205,165)],fill=(46,102,157,255),outline=INK),d.rectangle((45,82,190,176),fill=(92,176,211,255),outline=INK,width=8),d.rectangle((52,110,184,168),fill=(23,48,72,255),outline=INK,width=7),d.ellipse((75,127,91,143),fill=ICE_LIGHT),d.ellipse((145,127,161,143),fill=ICE_LIGHT)))
    part("body",(190,210),lambda d:(d.polygon([(32,22),(158,22),(181,194),(9,194)],fill=(37,78,130,255),outline=INK),d.polygon([(42,45),(148,45),(128,190),(62,190)],fill=(94,184,219,255),outline=INK)))
    part("arm_left",(100,190),lambda d:(d.rounded_rectangle((24,10,76,175),22,fill=(43,92,145,255),outline=INK,width=8),d.ellipse((20,145,80,187),fill=(122,209,234,255),outline=INK,width=7)))
    part("arm_right",(100,190),lambda d:(d.rounded_rectangle((24,10,76,175),22,fill=(43,92,145,255),outline=INK,width=8),d.ellipse((20,145,80,187),fill=(122,209,234,255),outline=INK,width=7)))
    part("leg_left",(95,150),lambda d:(d.rounded_rectangle((22,8,73,137),21,fill=(34,70,116,255),outline=INK,width=8),d.ellipse((10,105,82,148),fill=(103,194,224,255),outline=INK,width=7)))
    part("leg_right",(95,150),lambda d:(d.rounded_rectangle((22,8,73,137),21,fill=(34,70,116,255),outline=INK,width=8),d.ellipse((10,105,82,148),fill=(103,194,224,255),outline=INK,width=7)))

    image=canvas((190,410)); d=ImageDraw.Draw(image)
    d.polygon([(92,8),(163,94),(137,286),(55,286),(24,94)],fill=(143,47,39,255),outline=INK)
    d.polygon([(92,26),(141,103),(122,265),(67,265),(46,103)],fill=(215,83,65,255))
    d.rounded_rectangle((28,279,160,326),12,fill=(86,52,38,255),outline=INK,width=8)
    d.rounded_rectangle((72,319,112,402),10,fill=(118,72,45,255),outline=INK,width=7)
    save(WEAPONS,"meat_sword",image)

    image=canvas((250,205)); d=ImageDraw.Draw(image)
    d.ellipse((30,60,220,190),fill=(75,148,204,255),outline=INK,width=10)
    d.ellipse((48,34,118,115),fill=(84,163,218,255),outline=INK,width=8); d.ellipse((132,34,202,115),fill=(84,163,218,255),outline=INK,width=8)
    d.polygon([(52,58),(18,14),(74,40)],fill=(216,239,238,255),outline=INK); d.polygon([(198,58),(232,14),(176,40)],fill=(216,239,238,255),outline=INK)
    d.ellipse((78,71,172,153),fill=(181,221,235,255),outline=INK,width=8)
    d.ellipse((94,92,108,108),fill=INK); d.ellipse((142,92,156,108),fill=INK)
    d.ellipse((110,112,140,135),fill=(48,74,91,255),outline=INK,width=5)
    save(PETS,"blue_ox",image)


def main():
    environment(); character_and_items()
    print("Generated Ice Castle, Ice King, Meat Sword, and Blue Ox PNGs.")


if __name__ == "__main__": main()
