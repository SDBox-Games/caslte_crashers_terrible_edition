"""Generate editable PNG parts for Marsh, Corn Boss, and the swamp store."""

from pathlib import Path
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
LEVEL = ROOT / "assets" / "levels" / "marsh"
CHARS = ROOT / "assets" / "characters"
PETS = ROOT / "assets" / "pets"
ITEMS = ROOT / "assets" / "items"
WEAPONS = ROOT / "assets" / "weapons"
BOSS = ROOT / "assets" / "bosses" / "corn_boss"
INK = (31, 29, 25, 255)


def canvas(size):
    return Image.new("RGBA", size, (0, 0, 0, 0))


def save(folder, name, image):
    folder.mkdir(parents=True, exist_ok=True)
    image.save(folder / f"{name}.png")


def backdrop(name, store=False):
    image = canvas((1280, 720)); draw = ImageDraw.Draw(image)
    top = (63, 105, 103) if not store else (61, 72, 54)
    bottom = (170, 190, 122) if not store else (122, 104, 67)
    for y in range(720):
        t = y / 719
        draw.line((0, y, 1280, y), fill=tuple(int(a + (b-a)*t) for a, b in zip(top, bottom)) + (255,))
    if store:
        draw.rectangle((0, 95, 1280, 575), fill=(110, 78, 48, 255), outline=INK, width=12)
        for x in range(-80, 1360, 170):
            draw.ellipse((x, 70, x+210, 245), fill=(93, 117, 56, 255), outline=INK, width=7)
        draw.rectangle((0, 505, 1280, 720), fill=(86, 66, 43, 255))
    else:
        draw.polygon([(0,390),(180,310),(370,385),(610,285),(830,390),(1070,300),(1280,370),(1280,540),(0,540)], fill=(57,100,62,255))
        draw.rectangle((0, 500, 1280, 720), fill=(81, 141, 69, 255))
        draw.rectangle((0, 620, 1280, 720), fill=(68, 116, 59, 255))
    save(LEVEL, name, image)


def prop_art():
    image=canvas((330,420)); d=ImageDraw.Draw(image)
    d.rectangle((140,185,193,410),fill=(92,58,38,255),outline=INK,width=9)
    for box in ((15,55,205,270),(115,10,320,245),(35,5,195,195)):
        d.ellipse(box,fill=(52,117,57,255),outline=INK,width=8)
    save(LEVEL,"tree",image)
    image=canvas((470,350)); d=ImageDraw.Draw(image)
    d.rectangle((34,135,438,340),fill=(124,86,51,255),outline=INK,width=9)
    d.polygon([(10,145),(235,12),(462,145)],fill=(91,119,58,255),outline=INK)
    d.rounded_rectangle((182,205,282,342),30,fill=(48,38,31,255),outline=INK,width=8)
    d.rectangle((65,180,145,245),fill=(158,201,173,255),outline=INK,width=7)
    save(LEVEL,"house",image)
    image=canvas((150,205)); d=ImageDraw.Draw(image)
    d.rounded_rectangle((24,12,126,195),36,fill=(147,148,132,255),outline=INK,width=8)
    d.line((75,42,75,122),fill=(92,88,81,255),width=12); d.line((45,72,105,72),fill=(92,88,81,255),width=12)
    save(LEVEL,"grave",image)
    image=canvas((500,290)); d=ImageDraw.Draw(image)
    for x in range(0,500,95):
        d.rounded_rectangle((x,70+(x//95%2)*20,x+115,280),20,fill=(129,129,112,255),outline=INK,width=7)
    save(LEVEL,"stone_wall",image)
    image=canvas((400,300)); d=ImageDraw.Draw(image)
    d.polygon([(10,280),(105,105),(285,30),(390,280)],fill=(76,129,66,255),outline=INK)
    d.ellipse((45,180,360,315),fill=(58,111,54,255),outline=INK,width=6)
    save(LEVEL,"hill",image)
    image=canvas((350,280)); d=ImageDraw.Draw(image)
    d.rectangle((35,125,315,275),fill=(123,82,46,255),outline=INK,width=8)
    d.polygon([(10,135),(175,10),(340,135)],fill=(124,145,61,255),outline=INK)
    save(LEVEL,"hut",image)
    image=canvas((450,155)); d=ImageDraw.Draw(image)
    for x in range(25,445,105): d.rectangle((x,22,x+25,150),fill=(103,66,39,255),outline=INK,width=5)
    for y in (52,112): d.rectangle((5,y,445,y+20),fill=(117,74,42,255),outline=INK,width=5)
    save(LEVEL,"fence",image)
    image=canvas((120,160)); d=ImageDraw.Draw(image)
    d.polygon([(55,8),(82,54),(112,105),(61,151),(10,105),(39,53)],fill=(219,185,52,255),outline=INK)
    for y in (45,76,108): d.line((26,y,94,y),fill=(151,118,34,255),width=4)
    save(LEVEL,"corn_stalk",image)
    image=canvas((620,430)); d=ImageDraw.Draw(image)
    d.rectangle((55,145,565,420),fill=(135,72,42,255),outline=INK,width=12)
    d.polygon([(20,160),(310,18),(600,160)],fill=(158,63,42,255),outline=INK)
    d.rounded_rectangle((245,240,385,420),42,fill=(50,35,29,255),outline=INK,width=9)
    d.rectangle((85,205,190,300),fill=(197,221,178,255),outline=INK,width=8)
    save(LEVEL,"barn",image)
    image=canvas((120,105)); d=ImageDraw.Draw(image)
    d.ellipse((10,45,110,100),fill=(80,155,69,255),outline=INK,width=7); d.ellipse((30,13,93,73),fill=(95,176,78,255),outline=INK,width=6)
    d.ellipse((42,33,53,45),fill=INK); d.ellipse((70,33,81,45),fill=INK)
    save(LEVEL,"frog",image)


def knight_parts(folder, armor, accent, skin=(210,157,101,255), snake=False):
    target=CHARS/folder; target.mkdir(parents=True,exist_ok=True)
    for name in ("leg_left","leg_right"):
        im=canvas((64,105)); d=ImageDraw.Draw(im); d.rounded_rectangle((10,3,54,100),14,fill=armor,outline=INK,width=6); d.rectangle((7,76,58,102),fill=accent,outline=INK,width=5); im.save(target/f"{name}.png")
    for name in ("arm_left","arm_right"):
        im=canvas((62,104)); d=ImageDraw.Draw(im); d.rounded_rectangle((9,3,53,88),14,fill=armor,outline=INK,width=6); d.ellipse((11,73,52,103),fill=skin,outline=INK,width=5); im.save(target/f"{name}.png")
    im=canvas((120,140)); d=ImageDraw.Draw(im); d.rounded_rectangle((8,5,112,136),22,fill=armor,outline=INK,width=7)
    if snake: d.polygon([(20,26),(100,26),(78,124),(42,124)],fill=accent,outline=INK)
    else: d.line((30,68,90,68),fill=accent,width=10); d.line((60,28,60,118),fill=accent,width=10)
    im.save(target/"body.png")
    im=canvas((156,140)); d=ImageDraw.Draw(im); d.rounded_rectangle((13,22,143,136),25,fill=armor,outline=INK,width=8)
    if snake:
        d.ellipse((42,53,66,78),fill=(239,214,81,255),outline=INK,width=4); d.ellipse((90,53,114,78),fill=(239,214,81,255),outline=INK,width=4)
        d.line((78,78,78,122),fill=accent,width=10); d.polygon([(70,118),(86,118),(78,138)],fill=(190,52,45,255))
    else:
        d.rectangle((24,38,132,78),fill=skin,outline=INK,width=6); d.ellipse((48,52,60,65),fill=INK); d.ellipse((95,52,107,65),fill=INK)
        d.polygon([(16,35),(140,35),(124,9),(31,9)],fill=accent,outline=INK)
    im.save(target/"head.png")


def pickups():
    image=canvas((135,100)); d=ImageDraw.Draw(image)
    d.ellipse((10,38,102,94),fill=(156,93,52,255),outline=INK,width=7); d.ellipse((71,15,126,72),fill=(183,119,72,255),outline=INK,width=6)
    d.ellipse((88,31,97,41),fill=INK); d.ellipse((109,31,118,41),fill=INK)
    for x in (28,51,77,100): d.line((x,78,x-5,99),fill=INK,width=7)
    save(PETS,"pig",image)
    image=canvas((125,100)); d=ImageDraw.Draw(image)
    d.ellipse((12,25,82,92),fill=(115,68,37,255),outline=INK,width=7); d.arc((20,35,76,85),20,340,fill=(226,196,104,255),width=8)
    d.ellipse((71,52,119,91),fill=(191,164,87,255),outline=INK,width=6); d.ellipse((96,63,104,71),fill=INK)
    save(PETS,"snail",image)
    # Keep the shared Horn consistent with the Flooded Temple key art.
    image=canvas((240,185)); d=ImageDraw.Draw(image)
    outer=[(20,145),(54,101),(85,70),(122,44),(180,24),(222,35),(198,81),(165,119),(119,148),(68,165)]
    inner=[(35,142),(67,107),(95,82),(131,61),(174,44),(204,46),(181,74),(151,103),(111,128),(66,148)]
    d.polygon(outer,fill=INK); d.polygon(inner,fill=(212,150,37,255)); d.line(inner[:6],fill=(255,224,101,255),width=10,joint="curve")
    d.ellipse((169,12,233,80),fill=INK); d.ellipse((178,20,224,69),fill=(246,193,58,255)); d.ellipse((189,29,220,61),fill=(72,50,28,255),outline=INK,width=4)
    d.rounded_rectangle((66,110,107,174),10,fill=INK); d.rounded_rectangle((73,116,100,168),7,fill=(103,58,34,255))
    for y in (126,142,158): d.line((75,y,98,y-5),fill=(224,169,77,255),width=4)
    save(ITEMS,"horn",image)
    image=canvas((90,280)); d=ImageDraw.Draw(image)
    d.polygon([(44,5),(77,62),(64,190),(26,190),(13,62)],fill=(103,150,62,255),outline=INK)
    d.line((45,183,45,270),fill=(115,74,39,255),width=18); d.line((18,237,72,237),fill=(190,153,61,255),width=21)
    save(WEAPONS,"swamp_sword",image)


def corn_boss_parts():
    image=canvas((245,390)); d=ImageDraw.Draw(image)
    d.rounded_rectangle((45,12,200,380),70,fill=(225,187,45,255),outline=INK,width=10)
    for y in range(55,340,52):
        for x in range(73,185,38): d.ellipse((x-14,y-17,x+14,y+17),fill=(247,216,76,255),outline=(162,119,25,255),width=3)
    save(BOSS,"cob",image)
    for name, flip in (("leaf_left",False),("leaf_right",True)):
        image=canvas((250,320)); d=ImageDraw.Draw(image)
        points=[(220,300),(180,105),(18,15),(70,190)]
        if flip: points=[(250-x,y) for x,y in points]
        d.polygon(points,fill=(63,139,54,255),outline=INK); save(BOSS,name,image)
    image=canvas((205,135)); d=ImageDraw.Draw(image)
    d.polygon([(14,42),(76,18),(91,53),(116,53),(132,18),(192,42),(160,75),(45,75)],fill=(134,73,29,255),outline=INK)
    d.ellipse((43,50,81,91),fill=(214,46,41,255),outline=INK,width=5); d.ellipse((123,50,161,91),fill=(214,46,41,255),outline=INK,width=5)
    d.polygon([(51,105),(72,82),(91,107),(111,82),(132,107),(151,83),(165,120),(40,120)],fill=(241,226,177,255),outline=INK)
    save(BOSS,"face",image)
    image=canvas((180,60)); d=ImageDraw.Draw(image); d.line((8,50,166,9),fill=(112,80,34,255),width=10)
    for x in range(60,166,22): d.polygon([(x,34),(x+12,9),(x+21,29)],fill=(224,186,55,255),outline=INK)
    save(BOSS,"wheat",image)
    image=canvas((55,55)); d=ImageDraw.Draw(image); d.ellipse((5,7,50,50),fill=(250,240,203,255),outline=INK,width=5); save(BOSS,"popcorn",image)
    image=canvas((330,90)); d=ImageDraw.Draw(image); d.ellipse((8,20,322,86),fill=(103,73,43,255),outline=INK,width=8); save(BOSS,"mound",image)


def build():
    backdrop("cemetery_backdrop"); backdrop("village_backdrop"); backdrop("corn_backdrop"); backdrop("store_backdrop", True)
    prop_art(); knight_parts("snakey",(69,133,54,255),(205,180,59,255),snake=True); knight_parts("peasant",(137,87,49,255),(207,177,111,255))
    pickups(); corn_boss_parts()


if __name__ == "__main__":
    build()
