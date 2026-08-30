"""Generate editable PNG art for Snow World, its store, weapons, and pets."""

from pathlib import Path
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
LEVEL = ROOT / "assets" / "levels" / "snow_world"
PETS = ROOT / "assets" / "pets"
WEAPONS = ROOT / "assets" / "weapons"
INK = (12, 24, 35, 255)
SNOW = (235, 249, 252, 255)
ICE = (129, 211, 239, 255)
ICE_DARK = (69, 145, 187, 255)
WOOD = (110, 69, 45, 255)


def canvas(size):
    return Image.new("RGBA", size, (0, 0, 0, 0))


def save(folder, name, image):
    folder.mkdir(parents=True, exist_ok=True)
    image.save(folder / f"{name}.png")


def backdrop():
    image = canvas((1280, 720)); d = ImageDraw.Draw(image)
    top, bottom = (39, 76, 112), (166, 212, 231)
    for y in range(720):
        t = y / 719
        d.line((0, y, 1280, y), fill=tuple(int(a + (b-a)*t) for a,b in zip(top,bottom)) + (255,))
    d.ellipse((1000, 55, 1160, 215), fill=(225, 244, 249, 255), outline=INK, width=7)
    d.polygon([(0,455),(190,250),(365,430),(540,205),(760,430),(970,245),(1280,445),(1280,610),(0,610)], fill=(91,142,170,255))
    d.polygon([(0,510),(220,340),(390,500),(610,315),(820,500),(1050,330),(1280,485),(1280,640),(0,640)], fill=(142,190,211,255))
    for x, y in ((80,110),(235,205),(390,90),(545,170),(705,95),(860,220),(940,135),(1200,240)):
        d.ellipse((x, y, x+8, y+8), fill=SNOW)
    save(LEVEL, "backdrop", image)

    image = canvas((1280,720)); d = ImageDraw.Draw(image)
    for y in range(720):
        t=y/719; d.line((0,y,1280,y), fill=tuple(int(a+(b-a)*t) for a,b in zip((20,46,72),(103,165,195)))+(255,))
    d.rectangle((0,110,1280,720), fill=(95,145,170,255), outline=INK, width=10)
    for row in range(6):
        for col in range(12):
            x=col*120-(60 if row%2 else 0); y=120+row*76
            d.rounded_rectangle((x,y,x+112,y+68),10,fill=(113+row*4,170+col%2*7,196,255),outline=(67,118,151,255),width=5)
    d.rectangle((0,520,1280,720), fill=(218,241,247,255), outline=INK, width=9)
    d.polygon([(0,520),(170,475),(340,525),(520,470),(700,522),(900,474),(1090,523),(1280,476),(1280,555),(0,555)], fill=SNOW, outline=INK)
    save(LEVEL,"store_backdrop",image)

    image=canvas((1280,720)); d=ImageDraw.Draw(image)
    for y in range(720):
        t=y/719; d.line((0,y,1280,y),fill=tuple(int(a+(b-a)*t) for a,b in zip((18,46,79),(105,181,214)))+(255,))
    d.polygon([(150,570),(220,270),(355,270),(415,105),(535,105),(595,270),(730,270),(800,570)],fill=(127,205,232,255),outline=INK)
    d.polygon([(420,570),(470,350),(610,350),(650,190),(800,190),(850,350),(990,350),(1040,570)],fill=(182,232,246,255),outline=INK)
    d.ellipse((515,345,725,670),fill=(23,45,66,255),outline=INK,width=10)
    d.rectangle((0,560,1280,720),fill=SNOW,outline=INK,width=9)
    save(LEVEL,"ice_castle_backdrop",image)


def environment():
    image=canvas((440,220)); d=ImageDraw.Draw(image)
    d.rectangle((0,65,440,220),fill=(126,178,198,255),outline=INK,width=7)
    d.polygon([(0,70),(45,35),(92,68),(150,27),(220,66),(290,31),(355,70),(405,38),(440,66),(440,116),(0,116)],fill=SNOW,outline=INK)
    for x,y in ((42,145),(135,175),(245,135),(350,190)):
        d.ellipse((x,y,x+58,y+18),fill=(98,154,181,255))
    save(LEVEL,"snow_ground",image)

    image=canvas((280,430)); d=ImageDraw.Draw(image)
    d.rounded_rectangle((118,245,162,425),12,fill=WOOD,outline=INK,width=8)
    for pts in (((140,20),(30,220),(250,220)),((140,90),(10,290),(270,290)),((140,165),(0,365),(280,365))):
        d.polygon(pts,fill=(47,105,104,255),outline=INK)
        d.line((pts[1][0]+20,pts[1][1]-8,pts[2][0]-20,pts[2][1]-8),fill=SNOW,width=22)
    save(LEVEL,"snow_tree",image)

    image=canvas((270,190)); d=ImageDraw.Draw(image)
    d.polygon([(9,170),(25,55),(62,15),(93,52),(130,7),(167,52),(205,18),(246,55),(261,170)],fill=ICE,outline=INK)
    for x,y in ((55,70),(110,90),(180,65),(220,115)):
        d.line((x,y,x-18,y+58),fill=(212,247,252,255),width=7)
    save(LEVEL,"ice_wall",image)

    image=canvas((400,350)); d=ImageDraw.Draw(image)
    d.rectangle((50,130,350,335),fill=(102,142,159,255),outline=INK,width=10)
    d.polygon([(28,145),(200,28),(372,145)],fill=SNOW,outline=INK)
    d.polygon([(62,142),(200,62),(338,142)],fill=(61,112,138,255),outline=INK)
    d.rectangle((155,215,245,335),fill=(57,63,70,255),outline=INK,width=8)
    for x in (92,282): d.rectangle((x-30,190,x+30,250),fill=(246,207,91,255),outline=INK,width=7)
    save(LEVEL,"snow_house",image)

    image=canvas((100,230)); d=ImageDraw.Draw(image)
    d.line((50,215,50,65),fill=INK,width=34); d.arc((20,15,82,86),180,360,fill=INK,width=34)
    d.line((50,215,50,65),fill=(248,246,229,255),width=22); d.arc((26,21,76,80),180,360,fill=(248,246,229,255),width=22)
    for y in range(78,205,42): d.line((38,y,62,y+17),fill=(210,44,57,255),width=18)
    save(LEVEL,"candy_cane",image)

    image=canvas((380,320)); d=ImageDraw.Draw(image)
    d.rectangle((48,135,332,307),fill=(102,72,56,255),outline=INK,width=10)
    d.polygon([(24,150),(190,35),(356,150)],fill=(68,101,112,255),outline=INK)
    d.polygon([(45,142),(190,52),(335,142)],fill=SNOW,outline=INK)
    d.ellipse((135,180,245,345),fill=(31,40,48,255),outline=INK,width=9)
    save(LEVEL,"village_hut",image)

    image=canvas((400,350)); d=ImageDraw.Draw(image)
    d.rectangle((44,150,356,335),fill=(91,64,51,255),outline=INK,width=11)
    d.polygon([(18,163),(200,32),(382,163)],fill=SNOW,outline=INK)
    d.polygon([(55,153),(200,72),(345,153)],fill=(74,109,119,255),outline=INK)
    d.ellipse((132,190,268,370),fill=(25,37,47,255),outline=INK,width=10)
    d.ellipse((165,235,185,251),fill=(252,224,82,255)); d.ellipse((215,235,235,251),fill=(252,224,82,255))
    d.line((95,205,155,275),fill=(199,223,226,255),width=8); d.line((305,195,245,275),fill=(199,223,226,255),width=8)
    save(LEVEL,"yeti_hut",image)

    image=canvas((620,590)); d=ImageDraw.Draw(image)
    d.polygon([(20,565),(45,255),(120,140),(190,190),(255,50),(325,175),(405,85),(470,210),(550,145),(600,565)],fill=(116,203,235,255),outline=INK)
    d.polygon([(155,565),(175,320),(235,245),(310,230),(385,270),(445,345),(465,565)],fill=(25,48,69,255),outline=INK)
    for x,y in ((94,290),(210,175),(355,205),(490,270)):
        d.line((x,y,x-30,y+100),fill=(218,249,253,255),width=13)
    save(LEVEL,"ice_cave",image)

    image=canvas((80,80)); d=ImageDraw.Draw(image)
    d.ellipse((6,7,74,73),fill=SNOW,outline=INK,width=7); d.arc((15,13,63,54),190,330,fill=(171,220,235,255),width=6)
    save(LEVEL,"snowball",image)

    image=canvas((240,210)); d=ImageDraw.Draw(image)
    d.rounded_rectangle((16,55,224,198),18,fill=(81,119,139,255),outline=INK,width=9)
    d.polygon([(8,65),(120,10),(232,65)],fill=SNOW,outline=INK)
    d.rectangle((48,110,192,165),fill=(151,207,225,255),outline=INK,width=7)
    save(LEVEL,"shop_plinth",image)


def pets_and_weapons():
    image=canvas((230,210)); d=ImageDraw.Draw(image)
    d.ellipse((35,55,195,190),fill=(233,246,249,255),outline=INK,width=10)
    d.ellipse((53,24,112,100),fill=(225,241,245,255),outline=INK,width=8); d.ellipse((118,24,177,100),fill=(225,241,245,255),outline=INK,width=8)
    d.ellipse((66,54,164,151),fill=(133,190,210,255),outline=INK,width=8)
    d.ellipse((86,87,101,103),fill=INK); d.ellipse((130,87,145,103),fill=INK)
    d.polygon([(110,110),(120,120),(100,120)],fill=(47,66,78,255))
    d.line((30,152,7,182),fill=INK,width=13); d.line((200,152,223,182),fill=INK,width=13)
    save(PETS,"yeti",image)

    image=canvas((240,190)); d=ImageDraw.Draw(image)
    d.ellipse((45,62,193,176),fill=(220,102,43,255),outline=INK,width=10)
    d.polygon([(60,80),(48,12),(112,62)],fill=(220,102,43,255),outline=INK); d.polygon([(178,80),(192,12),(128,62)],fill=(220,102,43,255),outline=INK)
    d.ellipse((78,70,160,147),fill=(245,222,177,255),outline=INK,width=7)
    d.ellipse((95,88,107,102),fill=INK); d.ellipse((132,88,144,102),fill=INK)
    d.polygon([(119,108),(129,117),(109,117)],fill=(47,47,43,255))
    d.polygon([(43,140),(5,100),(17,163),(67,171)],fill=(245,222,177,255),outline=INK)
    save(PETS,"fox",image)

    image=canvas((170,420)); d=ImageDraw.Draw(image)
    d.polygon([(85,8),(128,88),(110,300),(60,300),(42,88)],fill=(36,38,48,255),outline=INK)
    d.polygon([(85,30),(108,96),(98,270),(72,270),(62,96)],fill=(176,30,43,255))
    d.rounded_rectangle((24,292,146,332),12,fill=(42,42,49,255),outline=INK,width=8)
    d.rounded_rectangle((70,325,100,412),9,fill=(112,68,43,255),outline=INK,width=7)
    save(WEAPONS,"black_red_sword",image)

    image=canvas((180,400)); d=ImageDraw.Draw(image)
    d.polygon([(84,15),(155,85),(136,250),(92,310),(45,275),(54,80)],fill=(203,215,217,255),outline=INK)
    d.line((83,35,69,252),fill=(245,252,251,255),width=12)
    d.rounded_rectangle((45,284,135,332),13,fill=(88,57,43,255),outline=INK,width=8)
    d.rounded_rectangle((72,325,108,392),10,fill=(112,70,45,255),outline=INK,width=7)
    save(WEAPONS,"butcher_knife",image)


def main():
    backdrop(); environment(); pets_and_weapons()
    print("Generated Snow World, Snow Store, pet, and weapon PNGs.")


if __name__ == "__main__":
    main()
