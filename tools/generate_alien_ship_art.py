"""Generate editable PNG parts for Alien Ship and its escape cutscenes."""

from pathlib import Path
from PIL import Image, ImageDraw

from generate_deserts_art import canvas, character_parts, outlined


ROOT = Path(__file__).resolve().parents[1]
LEVEL = ROOT / "assets" / "levels" / "alien_ship"


def save(name, image):
    LEVEL.mkdir(parents=True, exist_ok=True)
    image.save(LEVEL / f"{name}.png")


def build():
    LEVEL.mkdir(parents=True, exist_ok=True)
    ink = (13, 24, 28, 255)

    im = canvas((1280, 720)); d = ImageDraw.Draw(im)
    for y in range(720):
        t = y / 720
        d.line((0, y, 1280, y), fill=(int(18+19*t), int(41+31*t), int(48+32*t), 255))
    d.rectangle((0, 92, 1280, 555), fill=(52, 75, 78, 255), outline=ink, width=12)
    for x in range(-70, 1380, 185):
        d.polygon([(x, 105), (x+130, 105), (x+164, 165), (x+130, 225), (x, 225), (x-34, 165)], fill=(60, 91, 92, 255), outline=(28,49,52,255))
        d.ellipse((x+43, 135, x+87, 179), fill=(91, 246, 137, 255), outline=ink, width=5)
    d.rectangle((0, 555, 1280, 720), fill=(70, 80, 78, 255), outline=ink, width=10)
    for x in range(-80, 1360, 160):
        d.line((x, 560, x+90, 720), fill=(39, 50, 50, 255), width=8)
        d.line((x+80, 560, x+170, 720), fill=(112, 125, 116, 255), width=3)
    save("backdrop", im)

    im=canvas((150,430)); d=ImageDraw.Draw(im)
    outlined(d,(17,12,133,418),(54,66,69,255),22,8,ink)
    for y in (62,142,222,302):
        d.ellipse((42,y,108,y+66),fill=(135,244,172,255),outline=ink,width=6)
    save("laser_emitter",im)
    im=canvas((125,450)); d=ImageDraw.Draw(im)
    for x,color,width in ((62,(74,255,126,75),68),(62,(83,255,137,160),34),(62,(224,255,232,255),9)):
        d.line((x,7,x,443),fill=color,width=width)
    save("laser_beam",im)
    im=canvas((180,165)); d=ImageDraw.Draw(im)
    outlined(d,(8,9,172,157),(61,77,76,255),18,8,ink)
    d.ellipse((46,32,134,120),fill=(82,255,125,255),outline=ink,width=8)
    d.line((18,134,160,134),fill=(128,151,142,255),width=7)
    save("laser_box",im)
    im=canvas((180,165)); d=ImageDraw.Draw(im)
    outlined(d,(8,9,172,157),(45,51,52,255),18,8,ink)
    d.ellipse((46,32,134,120),fill=(51,65,61,255),outline=ink,width=8)
    d.line((24,30,154,139),fill=(223,73,59,255),width=11)
    save("laser_box_broken",im)

    im=canvas((420,260)); d=ImageDraw.Draw(im)
    outlined(d,(9,50,411,250),(45,58,62,255),18,9,ink)
    d.polygon([(42,68),(377,68),(344,173),(74,173)],fill=(43,120,105,255),outline=ink)
    for x,c in ((95,(98,255,138,255)),(160,(238,205,63,255)),(225,(87,190,245,255)),(291,(238,77,61,255))):
        d.ellipse((x,100,x+30,130),fill=c,outline=ink,width=4)
    for x in range(76,350,47): d.line((x,188,x,232),fill=(111,132,127,255),width=7)
    save("control_console",im)
    im=canvas((230,215)); d=ImageDraw.Draw(im)
    outlined(d,(12,10,218,204),(35,49,54,255),20,8,ink)
    for y in range(29,185,7):
        for x in range(30,201,10):
            shade=72+((x*19+y*13)%95); d.rectangle((x,y,x+7,y+4),fill=(shade,shade,shade,255))
    save("static_screen",im)

    im=canvas((940,390)); d=ImageDraw.Draw(im)
    outlined(d,(8,8,932,382),(33,55,65,255),35,12,ink)
    d.rectangle((34,34,906,356),fill=(111,190,221,255))
    d.ellipse((700,62,835,197),fill=(255,235,142,255))
    d.polygon([(35,250),(220,175),(405,257),(610,150),(905,244),(905,356),(35,356)],fill=(187,132,70,255))
    d.polygon([(35,290),(260,227),(475,307),(715,218),(905,279),(905,356),(35,356)],fill=(224,178,91,255))
    save("desert_window",im)

    im=canvas((520,300)); d=ImageDraw.Draw(im)
    # Sad antenna alien icon.
    d.line((205,68,165,18),fill=(144,255,174,255),width=10); d.line((315,68,356,18),fill=(144,255,174,255),width=10)
    d.ellipse((151,50,369,224),outline=(144,255,174,255),width=13)
    d.ellipse((202,104,230,132),fill=(144,255,174,255)); d.ellipse((290,104,318,132),fill=(144,255,174,255))
    d.arc((211,133,309,207),190,350,fill=(144,255,174,255),width=10)
    # Stylized Galactic-alphabet warning glyphs: header then subtitle.
    header=[(87,244),(128,229),(170,247),(213,228),(257,246),(301,228),(345,247),(389,229),(432,245)]
    for i,(x,y) in enumerate(header):
        d.line((x,y,x+18,y+25),fill=(255,105,75,255),width=6); d.ellipse((x+10,y-7,x+24,y+7),outline=(255,105,75,255),width=4)
    for i,x in enumerate(range(120,420,25)):
        d.arc((x,274-(i%2)*5,x+20,296),0,270,fill=(216,237,217,255),width=3)
    save("intruder_glass",im)

    im=canvas((170,230)); d=ImageDraw.Draw(im)
    outlined(d,(24,82,146,222),(47,61,63,255),25,8,ink)
    d.ellipse((29,8,141,119),fill=(79,99,98,255),outline=ink,width=8)
    d.rectangle((47,104,123,197),fill=(63,75,75,255),outline=ink,width=6)
    save("alien_seat",im)
    im=canvas((135,155)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((54,55,81,151),12,fill=(99,68,39,255),outline=ink,width=5)
    for level,(left,right) in enumerate(((17,118),(29,106),(41,94))):
        y=38+level*28; d.polygon([(67,8+level*8),(left,y),(right,y)],fill=(65+level*10,138+level*18,69+level*6,255),outline=ink)
    save("tree_ornament",im)
    for name,look in (("rat_idle",0),("rat_look",1)):
        im=canvas((145,105)); d=ImageDraw.Draw(im)
        d.ellipse((20,32,115,96),fill=(137,151,145,255),outline=ink,width=6)
        d.ellipse((82,20,137,70),fill=(157,170,162,255),outline=ink,width=5)
        d.ellipse((89,9,110,32),fill=(188,127,137,255),outline=ink,width=4)
        eye_x=121 if look else 111; d.ellipse((eye_x,35,eye_x+9,44),fill=(17,24,24,255))
        d.line((30,75,3,54),fill=(173,126,132,255),width=5)
        save(name,im)
    for name,on in (("alarm_off",False),("alarm_on",True)):
        im=canvas((145,175)); d=ImageDraw.Draw(im)
        d.rectangle((48,104,97,169),fill=(51,61,62,255),outline=ink,width=7)
        d.pieslice((20,15,125,123),180,360,fill=(252,67,50,255) if on else (89,53,50,255),outline=ink,width=7)
        if on:
            for y in (11,43,75): d.arc((3,y,142,y+72),190,350,fill=(255,188,84,255),width=6)
        save(name,im)

    im=canvas((240,235)); d=ImageDraw.Draw(im)
    outlined(d,(39,74,201,225),(225,229,215,255),28,9,ink)
    d.ellipse((25,35,215,143),fill=(215,222,210,255),outline=ink,width=9)
    d.ellipse((66,61,174,121),fill=(56,78,72,255),outline=ink,width=7)
    save("toilet",im)
    im=canvas((520,145)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((55,59,465,91),14,fill=(92,99,97,255),outline=ink,width=7)
    for x in (13,65,103,375,413,465): d.rounded_rectangle((x,28,x+42,123),8,fill=(55,61,61,255),outline=ink,width=5)
    # Render label as art so it stays attached to the weight texture.
    d.rectangle((211,18,309,126),fill=(238,207,63,255),outline=ink,width=7)
    d.text((224,57),"600KG",fill=ink,stroke_width=1)
    save("weight_600kg",im)
    im=canvas((280,255)); d=ImageDraw.Draw(im)
    outlined(d,(28,40,252,246),(54,70,70,255),27,9,ink)
    d.ellipse((73,8,207,136),fill=(75,104,98,255),outline=ink,width=8)
    d.polygon([(52,128),(228,128),(208,214),(72,214)],fill=(49,123,102,255),outline=ink)
    for x in (94,140,186): d.ellipse((x-13,155,x+13,181),fill=(113,255,140,255),outline=ink,width=4)
    save("ejection_chair",im)
    im=canvas((260,200)); d=ImageDraw.Draw(im)
    for i in range(8):
        x=20+(i*31)%205; y=50+(i*47)%105; d.ellipse((x,y,x+70,y+44),fill=(173,185,177,55+i*14))
    save("machine_smoke",im)
    im=canvas((205,100)); d=ImageDraw.Draw(im)
    outlined(d,(7,22,198,94),(59,68,67,255),13,7,ink)
    for x in range(28,185,31): d.line((x,34,x,82),fill=(27,40,40,255),width=9)
    save("floor_vent",im)
    im=canvas((190,300)); d=ImageDraw.Draw(im)
    for i in range(10):
        x=25+(i*47)%120; y=15+(i*71)%235; radius=23+(i%3)*10
        d.ellipse((x-radius,y-radius,x+radius,y+radius),fill=(214,231,220,35+i*12))
    save("vent_smoke",im)

    for name,occupied in (("escape_pod",False),("escape_pod_occupied",True)):
        im=canvas((250,360)); d=ImageDraw.Draw(im)
        d.ellipse((18,14,232,344),fill=(62,79,81,255),outline=ink,width=11)
        d.ellipse((49,50,201,235),fill=(88,210,210,180),outline=ink,width=9)
        d.rectangle((51,225,199,317),fill=(80,95,91,255),outline=ink,width=8)
        for x in (86,126,166): d.ellipse((x-10,264,x+10,284),fill=(103,255,137,255),outline=ink,width=3)
        if occupied:
            d.ellipse((83,91,167,177),fill=(244,218,56,255),outline=ink,width=7)
            d.ellipse((103,117,116,130),fill=ink); d.ellipse((136,117,149,130),fill=ink)
        save(name,im)
    im=canvas((320,320)); d=ImageDraw.Draw(im)
    d.polygon([(160,4),(192,91),(281,38),(232,127),(316,160),(230,192),(282,281),(193,231),(160,316),(127,231),(38,282),(91,192),(4,160),(92,127),(38,38),(127,91)],fill=(255,112,41,255),outline=(89,30,25,255))
    d.ellipse((83,83,237,237),fill=(255,222,74,255)); d.ellipse((127,127,193,193),fill=(255,250,213,255))
    save("ship_explosion",im)

    character_parts("alien_prisoner", (244,216,45,255), (61,145,64,255), alien=True)


if __name__ == "__main__":
    build()
