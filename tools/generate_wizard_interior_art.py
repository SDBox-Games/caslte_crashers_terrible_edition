"""Generate editable multipart art for Wizard Castle Interior and its first portal."""

from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
LEVEL = ROOT / "assets" / "levels" / "wizard_castle_interior"
FINAL = ROOT / "assets" / "levels" / "wizard_castle_final"
CULT = ROOT / "assets" / "characters" / "cult_minion"
WEAPONS = ROOT / "assets" / "weapons"
PETS = ROOT / "assets" / "pets"
INK = (8, 13, 23, 255)
PURPLE = (133, 54, 181, 255)
LILAC = (230, 129, 255, 255)
GREEN = (72, 220, 132, 255)
STONE = (57, 66, 77, 255)
STEEL = (119, 137, 148, 255)
WOOD = (104, 65, 42, 255)
CREAM = (246, 235, 207, 255)


def image(size):
    return Image.new("RGBA", size, (0, 0, 0, 0))


def save(name, art, folder=LEVEL):
    folder.mkdir(parents=True, exist_ok=True)
    art.save(folder / f"{name}.png")


def label(draw, xy, text, fill=CREAM):
    draw.text(xy, text, fill=fill, font=ImageFont.load_default(), anchor="mm", stroke_width=2, stroke_fill=INK)


def crystal(draw, points, fill=PURPLE):
    draw.polygon(points, fill=fill, outline=INK, width=7)
    left = min(x for x, _ in points); top = min(y for _, y in points)
    right = max(x for x, _ in points); bottom = max(y for _, y in points)
    draw.line((left + (right-left)*.45, top + 16, left + (right-left)*.35, bottom - 18), fill=LILAC, width=6)


def backdrop(name, top, bottom, green=False, gallery=False):
    art = image((1280, 720)); d = ImageDraw.Draw(art)
    for y in range(720):
        t = y / 719
        color = tuple(int(a + (b-a)*t) for a, b in zip(top, bottom)) + (255,)
        d.line((0, y, 1280, y), fill=color)
    for x in range(-40, 1320, 165):
        color = (43, 102, 75, 255) if green else (58, 43, 79, 255)
        d.polygon([(x, 70), (x+105, 18), (x+175, 155), (x+142, 555), (x+20, 555)], fill=color, outline=INK)
        crystal(d, [(x+23, 290), (x+62, 188), (x+92, 300), (x+72, 525), (x+35, 520)], GREEN if green else PURPLE)
    d.rectangle((0, 545, 1280, 720), fill=(48, 55, 61, 255) if gallery else (41, 50, 57, 255), outline=INK, width=8)
    for x in range(0, 1280, 120):
        d.line((x, 555, x+70, 720), fill=(72, 76, 85, 255), width=5)
    if gallery:
        d.rectangle((0, 85, 1280, 500), fill=(73, 54, 72, 255), outline=INK, width=10)
        d.rectangle((0, 480, 1280, 550), fill=(43, 31, 42, 255), outline=INK, width=8)
    save(name, art)


def make_backdrops():
    backdrop("crystal_hall_backdrop", (9, 31, 27), (29, 91, 63), green=True)
    backdrop("portal_hub_backdrop", (13, 32, 29), (35, 83, 59), green=True)
    backdrop("painter_arena_backdrop", (35, 17, 39), (88, 47, 77), gallery=True)
    backdrop("crystal_room_backdrop", (12, 30, 27), (35, 87, 62), green=True)


def props():
    art=image((135,230)); d=ImageDraw.Draw(art)
    d.ellipse((24,170,111,222), fill=(74,38,91,120)); crystal(d, [(67,8),(121,95),(93,203),(40,219),(12,105)], PURPLE)
    save("purple_flame",art)
    art=image((175,390)); d=ImageDraw.Draw(art)
    for i,(x,y,s) in enumerate(((88,20,1),(56,105,.75),(118,140,.68),(79,220,.82))):
        crystal(d, [(x,y),(x+45*s,y+75*s),(x+20*s,y+142*s),(x-25*s,y+120*s),(x-42*s,y+62*s)], PURPLE if i%2==0 else (183,72,221,255))
    save("purple_flame_tall",art)
    art=image((320,160)); d=ImageDraw.Draw(art)
    d.rounded_rectangle((18,28,302,105),18,fill=STEEL,outline=INK,width=10); d.rectangle((42,97,67,155),fill=STEEL,outline=INK,width=7); d.rectangle((253,97,278,155),fill=STEEL,outline=INK,width=7)
    save("steel_table",art)
    art=image((145,190)); d=ImageDraw.Draw(art)
    d.rounded_rectangle((23,13,122,101),16,fill=STEEL,outline=INK,width=9); d.rounded_rectangle((14,89,131,136),12,fill=(91,108,120,255),outline=INK,width=8); d.line((32,128,24,184),fill=INK,width=12); d.line((113,128,121,184),fill=INK,width=12)
    save("steel_chair",art)
    art=image((190,350)); d=ImageDraw.Draw(art)
    d.ellipse((42,15,148,113),fill=(220,213,187,255),outline=INK,width=8); d.ellipse((67,46,85,65),fill=INK); d.ellipse((105,46,123,65),fill=INK); d.line((95,75,95,96),fill=INK,width=7)
    d.line((95,110,95,247),fill=(222,215,188,255),width=22); d.line((95,145,28,209),fill=(222,215,188,255),width=17); d.line((95,145,161,196),fill=(222,215,188,255),width=17); d.line((94,238,48,337),fill=(222,215,188,255),width=19); d.line((95,238,140,337),fill=(222,215,188,255),width=19)
    save("wall_skeleton",art)
    art=image((360,390)); d=ImageDraw.Draw(art)
    d.polygon([(25,360),(335,360),(335,320),(75,320),(75,270),(285,270),(285,220),(125,220),(125,170),(240,170),(240,120),(175,120),(175,35),(25,35)],fill=(78,82,92,255),outline=INK)
    d.polygon([(175,35),(240,120),(240,170),(285,220),(285,270),(335,320),(335,360),(345,360),(345,15),(165,15)],fill=(35,32,46,210),outline=INK)
    save("blocked_stairs",art)
    art=image((420,360)); d=ImageDraw.Draw(art)
    d.polygon([(25,330),(48,120),(132,55),(215,112),(294,35),(394,121),(398,330)],fill=WOOD,outline=INK); d.polygon([(14,125),(126,28),(216,72),(300,10),(410,120),(375,145),(300,75),(220,138),(130,88),(49,159)],fill=(75,39,45,255),outline=INK); d.polygon([(130,188),(216,167),(221,329),(119,329)],fill=(24,22,30,255),outline=INK)
    save("floating_house",art)
    for i,pts in enumerate(([(5,30),(135,8),(149,42),(17,61)],[(8,8),(112,26),(94,63),(3,48)],[(12,44),(58,4),(123,26),(142,76),(67,65)]),1):
        art=image((155,85)); d=ImageDraw.Draw(art); d.polygon(pts,fill=WOOD,outline=INK,width=5); save(f"floating_plank_{i}",art)
    art=image((340,280)); d=ImageDraw.Draw(art)
    d.polygon([(17,121),(88,28),(207,12),(316,93),(298,221),(204,265),(76,237)],fill=(74,77,92,255),outline=INK); crystal(d,[(168,41),(224,116),(199,225),(141,236),(110,129)],PURPLE)
    save("floating_stone",art)
    art=image((90,75)); d=ImageDraw.Draw(art); d.polygon([(7,31),(26,7),(72,10),(84,46),(55,69),(16,63)],fill=(83,85,98,255),outline=INK,width=5); save("orbit_stone",art)
    art=image((650,400)); d=ImageDraw.Draw(art)
    d.ellipse((20,25,630,380),fill=(22,9,52,255),outline=INK,width=15)
    for i in range(34):
        x=(i*97)%590+30; y=(i*53)%315+35; d.ellipse((x,y,x+10+i%3*4,y+10+i%3*4),fill=(219,121,255,210))
    save("sky_hole",art)
    art=image((310,470)); d=ImageDraw.Draw(art)
    crystal(d,[(155,10),(286,158),(249,416),(83,453),(21,174)],GREEN); d.ellipse((102,118,210,220),fill=(224,216,188,210),outline=INK,width=7); d.line((156,211,156,354),fill=(229,222,197,220),width=19); d.line((156,246,85,315),fill=(229,222,197,220),width=14); d.line((156,246,231,303),fill=(229,222,197,220),width=14)
    save("skeleton_crystal",art)
    art=image((420,370)); d=ImageDraw.Draw(art)
    d.polygon([(25,342),(45,130),(126,62),(212,114),(298,38),(399,139),(401,342)],fill=WOOD,outline=INK); d.polygon([(15,136),(120,30),(216,74),(301,10),(410,132),(376,160),(300,76),(218,142),(124,98),(50,169)],fill=(74,44,37,255),outline=INK); d.ellipse((283,210,340,268),fill=(222,215,190,255),outline=INK,width=6)
    save("wood_house",art)
    art=image((500,570)); d=ImageDraw.Draw(art)
    crystal(d,[(70,548),(18,235),(118,70),(182,190),(250,10),(320,185),(390,70),(482,245),(430,548)],GREEN); d.ellipse((126,190,374,650),fill=(17,24,31,255),outline=INK,width=12)
    save("crystal_arch",art)
    for open_state in (False,True):
        art=image((260,390)); d=ImageDraw.Draw(art)
        d.ellipse((18,30,242,365),fill=(28,20,45,255),outline=INK,width=12); d.ellipse((52,68,208,330),fill=(85,25,115,255) if open_state else (47,47,57,255),outline=(220,113,247,255) if open_state else (105,105,115,255),width=9)
        if open_state:
            for i in range(7): d.arc((66-i*3,83-i*2,194+i*3,315+i*2),i*.5,math.pi*1.3+i*.4,fill=(226,129,255,255),width=5)
        else:
            d.line((80,118,180,282),fill=(130,130,140,255),width=18); d.line((180,118,80,282),fill=(130,130,140,255),width=18)
        save("portal_open" if open_state else "portal_locked",art)
    art=image((530,190)); d=ImageDraw.Draw(art); d.ellipse((15,35,515,177),fill=(84,38,107,255),outline=INK,width=10); d.ellipse((75,63,455,155),fill=(155,69,178,255),outline=(232,131,255,255),width=7); save("purple_rug",art)
    art=image((360,480)); d=ImageDraw.Draw(art); d.rectangle((35,15,325,430),fill=(111,76,48,255),outline=INK,width=13); d.rectangle((65,46,295,400),fill=(240,227,196,255),outline=(63,42,35,255),width=8); d.line((100,350,268,100),fill=(215,71,103,255),width=12); d.line((92,100,272,348),fill=(70,151,225,255),width=12); save("giant_canvas",art)
    art=image((280,110)); d=ImageDraw.Draw(art); d.rounded_rectangle((12,20,268,92),18,fill=(88,88,98,255),outline=INK,width=9); d.rectangle((40,8,66,105),fill=STEEL,outline=INK,width=6); d.rectangle((214,8,240,105),fill=STEEL,outline=INK,width=6); save("painter_lift",art)
    art=image((190,120)); d=ImageDraw.Draw(art); d.polygon([(22,83),(37,25),(153,25),(171,83),(151,110),(39,110)],fill=(83,68,69,255),outline=INK); d.rectangle((40,5,150,47),fill=(119,98,86,255),outline=INK,width=7); save("painter_toolbox_open",art)
    art=image((260,230)); d=ImageDraw.Draw(art); d.rounded_rectangle((15,18,245,213),22,fill=(35,32,43,255),outline=INK,width=11); d.rectangle((42,47,218,175),fill=(149,126,157,255),outline=INK,width=7); d.rectangle((88,210,172,228),fill=STEEL,outline=INK,width=6); save("paint_tv",art)
    art=image((190,125)); d=ImageDraw.Draw(art)
    for x,c in ((58,(222,76,83,255)),(132,(73,151,226,255))): d.ellipse((x-30,15,x+30,75),fill=c,outline=INK,width=5); d.line((x,74,x+int(math.sin(x)*18),112),fill=INK,width=8)
    save("painted_guys",art)
    for i,color in enumerate(((207,74,82,255),(77,146,222,255),(224,191,69,255),(89,191,113,255)),1):
        art=image((190,230)); d=ImageDraw.Draw(art); d.rectangle((15,12,175,218),fill=(104,71,45,255),outline=INK,width=9); d.rectangle((37,36,153,193),fill=(239,224,191,255),outline=INK,width=6); d.ellipse((58,67,132,141),fill=color,outline=INK,width=5); save(f"wall_canvas_{i}",art)
    art=image((240,190)); d=ImageDraw.Draw(art); d.rounded_rectangle((12,28,228,176),18,fill=(66,72,82,255),outline=INK,width=10); d.rectangle((36,8,204,46),fill=(92,101,113,255),outline=INK,width=7); save("painter_chest",art)
    for name,color,shape in (("coin",(240,187,56,255),"circle"),("bag",(171,116,55,255),"bag"),("gem",(74,224,193,255),"gem")):
        art=image((80,80)); d=ImageDraw.Draw(art)
        if shape=="circle": d.ellipse((9,9,71,71),fill=color,outline=INK,width=7)
        elif shape=="bag": d.polygon([(24,12),(56,12),(64,35),(70,68),(10,68),(16,35)],fill=color,outline=INK)
        else: d.polygon([(40,5),(72,30),(58,72),(22,72),(8,30)],fill=color,outline=INK)
        save(f"loot_{name}",art)
    for state in ("closed","open"):
        art=image((230,230)); d=ImageDraw.Draw(art); d.rounded_rectangle((12,12,218,218),18,fill=(31,38,49,255),outline=INK,width=10); d.ellipse((46,52,184,177),fill=(225,215,183,255),outline=INK,width=7); d.polygon([(54,79),(20,30),(91,58)],fill=(225,215,183,255),outline=INK); d.ellipse((91,86,118,113),fill=INK); d.arc((77,100,171,180),0,math.pi if state=="open" else .25,fill=INK,width=12); save(f"screen_eagle_{state}",art)
    for state in range(3):
        art=image((230,230)); d=ImageDraw.Draw(art); d.rounded_rectangle((12,12,218,218),18,fill=(31,38,49,255),outline=INK,width=10)
        if state==1: d.arc((52,55,178,203),math.pi,math.tau,fill=(184,225,113,255),width=27)
        elif state==2: d.arc((52,30,178,178),0,math.pi,fill=(184,225,113,255),width=27)
        else: d.line((52,115,180,115),fill=(184,225,113,255),width=27)
        save(f"screen_worm_{state}",art)
    art=image((430,430)); d=ImageDraw.Draw(art); d.polygon([(25,410),(405,410),(405,350),(75,350),(75,290),(345,290),(345,230),(130,230),(130,170),(280,170),(280,110),(190,110),(190,25),(25,25)],fill=(103,110,122,255),outline=INK); save("exit_stairs",art)
    art=image((330,430)); d=ImageDraw.Draw(art); crystal(d,[(165,8),(306,140),(264,391),(76,416),(18,155)],(85,224,145,255)); crystal(d,[(165,55),(236,155),(212,348),(111,363),(81,164)],PURPLE); save("seal_crystal",art)


def painting(name):
    art=image((240,240)); d=ImageDraw.Draw(art); color={"unicorn":(234,225,224,255),"carrot":(241,124,43,255),"clown":(229,77,97,255),"red":(213,51,55,255),"green":(68,185,95,255),"cat":(238,185,73,255),"shakey":(145,100,180,255),"octopus":(173,73,161,255),"elephant":(148,157,171,255),"snail":(114,178,96,255),"scissors":(192,200,210,255)}[name]
    if name=="carrot": d.polygon([(120,40),(184,92),(122,224),(59,92)],fill=color,outline=INK); d.polygon([(88,54),(68,7),(116,43),(137,5),(146,51)],fill=GREEN,outline=INK)
    elif name=="octopus": d.ellipse((47,28,193,166),fill=color,outline=INK,width=7); [d.arc((25+i*38,130,105+i*32,229),0,math.pi,fill=color,width=20) for i in range(4)]
    elif name=="snail": d.ellipse((72,51,214,190),fill=color,outline=INK,width=7); d.ellipse((19,117,110,205),fill=(218,191,113,255),outline=INK,width=7); d.arc((107,77,184,157),0,math.tau,fill=INK,width=7)
    elif name=="scissors": d.ellipse((28,30,102,104),outline=color,width=20); d.ellipse((138,30,212,104),outline=color,width=20); d.line((80,90,188,220),fill=color,width=24); d.line((160,90,52,220),fill=color,width=24)
    else:
        d.ellipse((38,43,202,191),fill=color,outline=INK,width=8); d.ellipse((76,86,98,110),fill=INK); d.ellipse((142,86,164,110),fill=INK); d.arc((81,101,163,164),0,math.pi,fill=INK,width=8)
        if name=="unicorn": d.polygon([(120,49),(143,2),(157,57)],fill=(244,201,65,255),outline=INK)
        elif name=="cat": d.polygon([(48,67),(58,17),(91,53)],fill=color,outline=INK); d.polygon([(149,54),(182,17),(193,72)],fill=color,outline=INK)
        elif name=="elephant": d.line((121,143,121,224),fill=color,width=35); d.ellipse((7,68,76,168),fill=color,outline=INK,width=6); d.ellipse((164,68,233,168),fill=color,outline=INK,width=6)
        elif name=="clown": d.ellipse((30,30,72,72),fill=(74,154,230,255),outline=INK); d.ellipse((168,30,210,72),fill=(242,195,55,255),outline=INK); d.ellipse((106,107,134,135),fill=(226,48,57,255),outline=INK)
    save(f"painting_{name}",art)


def cult_minion():
    art=image((160,155)); d=ImageDraw.Draw(art); d.polygon([(80,4),(148,84),(127,149),(33,149),(12,84)],fill=(40,27,53,255),outline=INK); d.ellipse((53,67,107,112),fill=LILAC,outline=INK,width=7); d.ellipse((70,79,90,101),fill=INK); save("head",art,CULT)
    art=image((125,145)); d=ImageDraw.Draw(art); d.polygon([(22,8),(103,8),(117,137),(8,137)],fill=(44,29,58,255),outline=INK); d.polygon([(63,41),(94,83),(63,118),(31,83)],fill=PURPLE,outline=INK); save("body",art,CULT)
    for name,flip in (("arm_left",False),("arm_right",True)):
        art=image((62,110)); d=ImageDraw.Draw(art); d.rounded_rectangle((12,4,50,96),14,fill=(47,31,61,255),outline=INK,width=6); d.ellipse((12,82,50,108),fill=(172,124,170,255),outline=INK,width=5); save(name,art.transpose(Image.Transpose.FLIP_LEFT_RIGHT) if flip else art,CULT)
    for name,flip in (("leg_left",False),("leg_right",True)):
        art=image((65,112)); d=ImageDraw.Draw(art); d.rounded_rectangle((14,4,50,100),13,fill=(34,26,45,255),outline=INK,width=6); d.ellipse((7,85,57,110),fill=(70,46,69,255),outline=INK,width=5); save(name,art.transpose(Image.Transpose.FLIP_LEFT_RIGHT) if flip else art,CULT)


def later_boss_backdrops():
    art=image((1280,720)); d=ImageDraw.Draw(art)
    d.rectangle((0,0,1280,720),fill=(16,8,14,255))
    d.rectangle((0,535,1280,720),fill=(29,20,24,255),outline=INK,width=9)
    for x in range(-60,1340,190):
        crystal(d,[(x+85,505),(x+130,390),(x+166,510),(x+145,548),(x+103,548)],(158,34,48,255))
    save("cyclops_arena_backdrop",art)

    art=image((1280,720)); d=ImageDraw.Draw(art)
    d.rectangle((0,0,1280,720),fill=(43,46,54,255))
    for x in range(0,1280,160):
        d.rectangle((x,65,x+145,535),fill=(67,72,82,255),outline=INK,width=8)
        d.ellipse((x+47,115,x+98,166),fill=(136,72,173,255),outline=INK,width=5)
        d.line((x+18,280,x+130,280),fill=(105,112,122,255),width=7)
    d.rectangle((0,530,1280,720),fill=(34,37,43,255),outline=INK,width=9)
    save("necromancer_arena_backdrop",art)

    art=image((1280,720)); d=ImageDraw.Draw(art)
    d.rectangle((0,0,1280,720),fill=(22,13,38,255))
    for x in range(-30,1300,180):
        crystal(d,[(x+85,525),(x+130,318),(x+165,520),(x+145,555),(x+105,555)],PURPLE)
    d.rectangle((0,545,1280,720),fill=(54,57,68,255),outline=INK,width=9)
    save("final_approach_backdrop",art)

    art=image((1280,720)); d=ImageDraw.Draw(art)
    d.rectangle((0,0,1280,720),fill=(2,2,10,255))
    for i in range(30):
        x=(i*211)%1280; y=(i*83)%520
        d.ellipse((x,y,x+5+i%4*3,y+5+i%4*3),fill=(166,71,221,160))
    d.rectangle((0,545,1280,720),fill=(17,16,27,255),outline=INK,width=9)
    save("final_arena_backdrop",art)

    art=image((1280,720)); d=ImageDraw.Draw(art)
    for y in range(720):
        t=y/719; d.line((0,y,1280,y),fill=(int(60+80*t),int(90+80*t),int(130+60*t),255))
    d.rectangle((0,525,1280,720),fill=(98,80,67,255),outline=INK,width=9)
    d.polygon([(0,370),(180,245),(350,365),(560,210),(760,355),(1010,225),(1280,380),(1280,525),(0,525)],fill=(83,112,103,255),outline=INK)
    for x in range(80,1280,150):
        d.ellipse((x,75,x+18,93),fill=(244,195,64,255)); d.line((x+9,93,x+9,155),fill=(231,231,213,255),width=4)
    save("celebration_backdrop",art)

    # One continuous vertical environment: the green crystal lift room is at
    # the bottom, a black shaft connects it, and the Final Boss arena occupies
    # the top.  The renderer scrolls this single PNG instead of cutting scenes.
    art=image((1280,1560)); d=ImageDraw.Draw(art)
    d.rectangle((0,0,1280,720),fill=(2,3,10,255))
    for i in range(34):
        x=(i*211)%1280; y=(i*83)%520
        d.ellipse((x,y,x+6+i%4*3,y+6+i%4*3),fill=(158,65,216,150))
    d.rectangle((0,545,1280,720),fill=(17,16,27,255),outline=INK,width=9)
    d.rectangle((0,720,1280,880),fill=(5,8,13,255),outline=INK,width=10)
    for x in range(70,1280,190):
        d.line((x,720,x+95,880),fill=(46,36,59,255),width=8)
    for y in range(880,1560):
        t=(y-880)/679
        d.line((0,y,1280,y),fill=(int(10+18*t),int(38+43*t),int(31+29*t),255))
    for x in range(-55,1340,165):
        d.polygon([(x,950),(x+105,895),(x+176,1035),(x+142,1392),(x+20,1392)],fill=(37,101,73,255),outline=INK)
        crystal(d,[(x+25,1210),(x+65,1082),(x+96,1218),(x+73,1382),(x+37,1372)],GREEN)
    d.rectangle((0,1380,1280,1560),fill=(39,54,52,255),outline=INK,width=9)
    save("vertical_crystal_backdrop",art,FINAL)

    art=image((1280,720)); d=ImageDraw.Draw(art)
    d.rectangle((0,0,1280,720),fill=(86,82,77,255))
    d.rectangle((0,65,1280,520),fill=(133,126,113,255),outline=INK,width=10)
    for x in range(40,1280,205):
        d.rectangle((x,105,x+150,260),fill=(105,70,47,255),outline=INK,width=8)
        d.rectangle((x+13,118,x+137,172),fill=(164,120,76,255),outline=INK,width=5)
        d.rectangle((x+13,186,x+137,240),fill=(164,120,76,255),outline=INK,width=5)
    for x in (235,640,1045):
        d.line((x,55,x,510),fill=(76,71,68,255),width=13)
        d.ellipse((x-34,35,x+34,103),fill=(243,188,66,255),outline=INK,width=7)
    d.rectangle((0,520,1280,720),fill=(96,76,59,255),outline=INK,width=10)
    for x in range(0,1280,140):
        d.line((x,530,x+80,720),fill=(126,101,78,255),width=5)
    save("castle_barracks_backdrop",art,FINAL)


def later_boss_props():
    art=image((220,280)); d=ImageDraw.Draw(art); crystal(d,[(110,5),(202,105),(172,258),(48,270),(11,118)],(174,39,51,255)); save("red_ground_crystal",art)
    art=image((500,300)); d=ImageDraw.Draw(art)
    d.ellipse((35,75,245,220),outline=(225,216,187,255),width=35); d.ellipse((260,15,460,186),outline=(225,216,187,255),width=32); d.line((70,220,430,96),fill=(225,216,187,255),width=38); d.line((70,220,430,96),fill=INK,width=7)
    save("giant_bones",art)
    for name,inside in (("golden_entrance",(29,20,35,255)),("golden_exit",(84,31,103,255))):
        art=image((440,560)); d=ImageDraw.Draw(art); d.ellipse((25,15,415,630),fill=(205,143,35,255),outline=INK,width=13); d.ellipse((82,85,358,620),fill=inside,outline=(250,205,79,255),width=11); [d.ellipse((70+i*75,55,95+i*75,80),fill=(255,232,137,255)) for i in range(4)]; save(name,art)
    for state in ("closed","open"):
        art=image((300,160)); d=ImageDraw.Draw(art); d.ellipse((15,55,285,145),fill=(82,48,33,255),outline=INK,width=10)
        if state=="open": d.ellipse((50,75,250,142),fill=(12,9,14,255),outline=INK,width=7); d.polygon([(35,78),(250,20),(275,72),(58,130)],fill=(109,66,39,255),outline=INK)
        else: d.ellipse((35,40,265,130),fill=(109,66,39,255),outline=INK,width=8)
        save(f"brown_hatch_{state}",art)
    art=image((230,320)); d=ImageDraw.Draw(art); d.ellipse((20,10,210,305),fill=(99,75,66,255),outline=INK,width=10); d.polygon([(45,80),(115,30),(190,83),(205,265),(25,265)],fill=(117,87,73,255),outline=INK); save("cyclops_body",art)
    art=image((220,220)); d=ImageDraw.Draw(art); d.ellipse((15,15,205,205),fill=(111,84,73,255),outline=INK,width=10); d.ellipse((60,65,160,145),fill=CREAM,outline=INK,width=8); d.ellipse((93,88,130,125),fill=INK); d.arc((55,124,166,190),math.pi,math.tau,fill=INK,width=9); save("cyclops_head",art)
    art=image((105,250)); d=ImageDraw.Draw(art); d.rounded_rectangle((20,8,85,205),27,fill=(109,82,71,255),outline=INK,width=9); d.ellipse((7,180,98,245),fill=(109,82,71,255),outline=INK,width=8); save("cyclops_arm",art)
    art=image((220,430)); d=ImageDraw.Draw(art); d.rounded_rectangle((16,12,204,414),28,fill=(67,49,63,255),outline=INK,width=11); d.polygon([(42,54),(178,54),(196,185),(110,245),(25,184)],fill=(115,74,105,255),outline=INK); d.line((110,75,110,370),fill=(222,130,247,255),width=8); save("cyclops_coffin",art); save("giant_coffin",art,WEAPONS)
    art=image((240,350)); d=ImageDraw.Draw(art); d.ellipse((20,15,220,330),fill=(213,235,241,135),outline=(245,255,255,190),width=8); d.ellipse((65,62,175,155),fill=(245,255,255,180),outline=INK,width=5); d.ellipse((96,88,133,125),fill=INK); save("cyclops_ghost",art)
    art=image((150,170)); d=ImageDraw.Draw(art); d.polygon([(16,20),(134,20),(146,161),(8,161)],fill=(91,49,62,235),outline=INK); d.line((28,65,122,65),fill=(212,188,131,255),width=7); save("buddy_clothes",art)
    art=image((150,230)); d=ImageDraw.Draw(art); d.ellipse((20,8,130,218),fill=(223,239,245,130),outline=(248,255,255,190),width=7); d.ellipse((47,40,103,100),fill=(246,248,236,180),outline=INK,width=5); save("buddy_ghost",art)
    art=image((250,180)); d=ImageDraw.Draw(art); d.rounded_rectangle((12,38,238,169),20,fill=(174,114,36,255),outline=INK,width=10); d.rectangle((30,12,220,72),fill=(226,165,51,255),outline=INK,width=9); d.ellipse((105,82,145,122),fill=PURPLE,outline=INK,width=5); save("boss_chest",art)
    art=image((250,180)); d=ImageDraw.Draw(art); d.rounded_rectangle((12,78,238,169),20,fill=(174,114,36,255),outline=INK,width=10); d.polygon([(22,79),(58,13),(221,13),(238,78)],fill=(226,165,51,255),outline=INK); d.ellipse((105,104,145,144),fill=PURPLE,outline=INK,width=5); save("boss_chest_open",art)
    for i,color in enumerate(((80,94,108,255),(115,83,65,255),(73,53,82,255)),1):
        art=image((230,150)); d=ImageDraw.Draw(art); d.ellipse((12,70,98,144),fill=(220,211,184,255),outline=INK,width=6); d.polygon([(70,130),(108,28),(180,44),(220,134)],fill=color,outline=INK); d.ellipse((150,66,217,138),fill=(225,216,188,255),outline=INK,width=6); save(f"corpse_pile_{i}",art)
    art=image((360,250)); d=ImageDraw.Draw(art); d.polygon([(180,128),(20,20),(62,166)],fill=(43,30,58,255),outline=INK); d.polygon([(180,128),(340,20),(298,166)],fill=(43,30,58,255),outline=INK); [d.line((180,128,35+i*35,43+i%2*80),fill=(164,83,204,255),width=5) for i in range(5)]; [d.line((180,128,325-i*35,43+i%2*80),fill=(164,83,204,255),width=5) for i in range(5)]; save("necromancer_wings",art)
    art=image((55,55)); d=ImageDraw.Draw(art); d.ellipse((5,5,50,50),fill=(211,102,242,140),outline=(245,189,255,220),width=5); save("soul_particle",art)
    art=image((150,190)); d=ImageDraw.Draw(art); d.ellipse((15,142,135,180),outline=(203,73,207,200),width=8); save("skeleton_hand_warning",art)
    art=image((150,220)); d=ImageDraw.Draw(art); d.line((75,210,75,95),fill=(228,220,194,255),width=26); [d.line((75,105,32+i*29,25+i%2*25),fill=(228,220,194,255),width=16) for i in range(4)]; save("skeleton_hand",art)
    art=image((125,125)); d=ImageDraw.Draw(art); d.ellipse((12,12,113,113),fill=(226,219,195,255),outline=INK,width=8); d.ellipse((35,42,55,64),fill=INK); d.ellipse((70,42,90,64),fill=INK); d.polygon([(62,62),(53,83),(72,83)],fill=INK); d.line((89,22,112,2),fill=(106,68,134,255),width=7); save("skeleton_bomb",art)
    art=image((120,90)); d=ImageDraw.Draw(art); d.ellipse((9,20,111,82),fill=(112,190,85,120),outline=(190,236,129,180),width=5); d.ellipse((35,3,85,46),fill=(159,218,104,120)); save("fart_cloud",art)
    art=image((170,720)); d=ImageDraw.Draw(art); d.rectangle((35,0,135,720),fill=(91,22,127,130)); d.rectangle((57,0,113,720),fill=(199,78,242,215)); d.rectangle((76,0,94,720),fill=(252,220,255,245)); d.ellipse((9,630,161,712),outline=(231,143,255,235),width=10); save("necromancer_summon_laser",art)
    art=image((125,390)); d=ImageDraw.Draw(art); d.polygon([(54,380),(72,380),(79,100),(47,100)],fill=(91,67,108,255),outline=INK); d.polygon([(62,8),(112,96),(62,137),(12,96)],fill=(198,85,224,255),outline=INK); d.ellipse((48,42,76,70),fill=CREAM,outline=INK,width=4); save("necromancer_sword",art,WEAPONS)
    art=image((300,130)); d=ImageDraw.Draw(art); d.ellipse((12,25,288,115),fill=(103,109,120,255),outline=INK,width=10); d.ellipse((55,44,245,99),fill=(54,59,68,255),outline=(166,173,184,255),width=7); save("gray_lift_pad",art)
    art=image((420,500)); d=ImageDraw.Draw(art); crystal(d,[(210,10),(388,180),(344,465),(76,480),(20,190)],(107,55,151,255)); d.ellipse((105,182,315,390),fill=(38,21,57,255),outline=LILAC,width=8); save("final_throne_crystal",art)
    art=image((190,250)); d=ImageDraw.Draw(art); crystal(d,[(95,5),(178,95),(152,236),(39,245),(9,107)],(202,42,61,255)); save("final_red_crystal",art)
    for name,color in (("bubble_blue",(50,191,255,95)),("bubble_red",(255,58,69,95))):
        art=image((360,360)); d=ImageDraw.Draw(art); d.ellipse((18,18,342,342),fill=color,outline=(color[0],color[1],color[2],230),width=12); d.arc((48,48,312,312),3.5,5.8,fill=CREAM,width=5); save(name,art)
    for name,color in (("final_ball",(73,40,91,255)),("final_ball_white",(245,245,239,255))):
        art=image((290,290)); d=ImageDraw.Draw(art); d.ellipse((12,12,278,278),fill=color,outline=INK,width=11); [d.arc((35+i*15,35+i*15,255-i*15,255-i*15),i*.6,math.pi+i*.8,fill=LILAC if name=="final_ball" else (220,214,200,255),width=7) for i in range(5)]; save(name,art)
    art=image((330,300)); d=ImageDraw.Draw(art); d.polygon([(165,12),(316,275),(14,275)],fill=(61,42,77,255),outline=INK); d.polygon([(165,58),(264,244),(66,244)],fill=(210,75,227,255),outline=INK); d.ellipse((128,142,158,172),fill=INK); d.ellipse((174,142,204,172),fill=INK); save("triangle_core",art)
    art=image((330,300)); d=ImageDraw.Draw(art); d.polygon([(165,12),(316,275),(14,275)],fill=(248,247,235,255),outline=INK); d.polygon([(165,58),(264,244),(66,244)],fill=(255,221,102,255),outline=INK); d.ellipse((128,142,158,172),fill=INK); d.ellipse((174,142,204,172),fill=INK); save("triangle_core_white",art)
    art=image((85,265)); d=ImageDraw.Draw(art); d.polygon([(42,4),(78,82),(61,246),(43,261),(18,240),(9,82)],fill=(88,55,104,255),outline=INK); [d.polygon([(18,80+i*45),(-3,101+i*45),(21,111+i*45)],fill=(221,91,227,255),outline=INK) for i in range(3)]; save("triangle_arm",art)
    art=image((85,265)); d=ImageDraw.Draw(art); d.polygon([(42,4),(78,82),(61,246),(43,261),(18,240),(9,82)],fill=(248,247,235,255),outline=INK); [d.polygon([(18,80+i*45),(-3,101+i*45),(21,111+i*45)],fill=(255,221,102,255),outline=INK) for i in range(3)]; save("triangle_arm_white",art)
    for name,color,spike in (("triangle_small_arm",(88,55,104,255),(221,91,227,255)),("triangle_small_arm_white",(248,247,235,255),(255,221,102,255))):
        art=image((190,90)); d=ImageDraw.Draw(art); d.rounded_rectangle((8,26,145,64),16,fill=color,outline=INK,width=7); d.polygon([(137,18),(188,45),(137,72)],fill=spike,outline=INK); d.polygon([(112,27),(139,3),(143,31)],fill=spike,outline=INK); d.polygon([(112,63),(139,87),(143,59)],fill=spike,outline=INK); save(name,art)
    art=image((120,620)); d=ImageDraw.Draw(art); d.rectangle((40,0,80,620),fill=(255,36,53,100)); d.rectangle((53,0,67,620),fill=(255,232,214,230)); save("red_sky_laser",art)
    for name,size in (("white_orb_large",100),("white_orb_small",55)):
        art=image((size,size)); d=ImageDraw.Draw(art); d.ellipse((5,5,size-5,size-5),fill=(250,248,235,255),outline=INK,width=max(4,size//12)); save(name,art)
    art=image((150,80)); d=ImageDraw.Draw(art); d.ellipse((8,18,142,68),outline=(244,77,63,220),width=9); d.ellipse((40,31,110,56),outline=(250,190,61,180),width=5); save("meteor_target",art)
    art=image((160,190)); d=ImageDraw.Draw(art); d.polygon([(80,5),(147,85),(124,177),(40,183),(12,92)],fill=(105,73,64,255),outline=INK); d.polygon([(45,52),(82,8),(113,56),(97,101),(55,101)],fill=(231,88,44,255),outline=INK); save("final_meteor",art)
    art=image((1280,230)); d=ImageDraw.Draw(art); d.polygon([(0,25),(160,52),(290,18),(430,80),(590,22),(740,75),(910,14),(1080,68),(1280,30),(1280,230),(0,230)],fill=(37,31,42,255),outline=INK); [d.line((x,45,x+80,205),fill=(110,73,126,255),width=8) for x in range(20,1280,150)]; save("crumbling_floor",art)
    art=image((300,330)); d=ImageDraw.Draw(art); crystal(d,[(150,6),(286,123),(240,305),(64,316),(13,135)],(108,219,161,255)); d.line((68,187,235,102),fill=(233,250,201,255),width=8); save("escape_crystal",art)
    art=image((120,140)); d=ImageDraw.Draw(art); d.ellipse((17,25,103,132),fill=(24,31,38,255),outline=INK,width=7); d.ellipse((30,10,90,67),fill=(26,32,39,255),outline=INK,width=6); d.ellipse((45,30,75,49),fill=CREAM); d.polygon([(47,53),(73,53),(60,68)],fill=(238,166,48,255),outline=INK); save("party_penguin",art)
    art=image((150,110)); d=ImageDraw.Draw(art); d.ellipse((15,18,135,102),fill=(225,162,89,255),outline=INK,width=7); d.polygon([(32,33),(20,2),(58,25)],fill=(225,162,89,255),outline=INK); d.polygon([(93,25),(130,2),(119,38)],fill=(225,162,89,255),outline=INK); d.ellipse((52,48,65,61),fill=INK); d.ellipse((87,48,100,61),fill=INK); save("flying_cat",art)
    art=image((170,145)); d=ImageDraw.Draw(art); d.ellipse((24,37,146,132),fill=(225,162,89,255),outline=INK,width=8); d.ellipse((46,10,126,85),fill=(225,162,89,255),outline=INK,width=8); d.polygon([(52,31),(48,1),(75,20)],fill=(225,162,89,255),outline=INK); d.polygon([(100,20),(128,1),(121,35)],fill=(225,162,89,255),outline=INK); d.ellipse((67,42,78,54),fill=INK); d.ellipse((96,42,107,54),fill=INK); d.arc((73,51,103,73),0,math.pi,fill=INK,width=4); d.line((25,86,2,61),fill=(225,162,89,255),width=16); save("cat",art,PETS)


def main():
    make_backdrops(); props(); later_boss_backdrops(); later_boss_props()
    for name in list(("unicorn","carrot","clown","red","green","cat","shakey","octopus","elephant","snail","scissors")): painting(name)
    cult_minion()
    print("Generated all Wizard Castle Interior portals, bosses, multipart effects, celebration, and character art.")


if __name__ == "__main__":
    main()
