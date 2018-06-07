import random
from PIL import Image,ImageDraw,ImageFont
from gi.repository import Gio
import pprint

#returns the path to the current wallpaper
def get_wallpaper():
    settings = Gio.Settings.new("org.gnome.desktop.background")
    uri = settings.get_string("picture-uri")
    return uri.strip('file')[3:]

def set_up(walllpaper,tasks):

    midx = int(round(wallpaper.size[0]/2,0))
    num = len(tasks)
    height = wallpaper.size[1]
    margin = 50
    txt_margin = 20

    #positions of all messages
    pos = [i*height/num for i in range(num)]
    pos = [p + (height-pos[-1])/2 for p in pos]

    # make a blank image for the text, initialized to transparent text color
    txt = Image.new('RGBA', wallpaper.size, (255,255,255,0))
    # get a font
    fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40)
    f1_size = 75
    fnt1 = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', f1_size)
    # get a drawing context
    draw = ImageDraw.Draw(txt)

    #draw rectangle to the right of the desktop
    draw.rectangle(((midx,margin), (wallpaper.size[0] - margin, wallpaper.size[1] - margin)), fill=(0,0,0,128))

    #write headers - urgent / important
    draw.text(( wallpaper.size[0] - 5*f1_size, margin), "Urgent", font=fnt1, fill=(255,0,0,255))
    draw.text(( wallpaper.size[0] - 6*f1_size, wallpaper.size[1] - margin - f1_size), "Important", font=fnt1, fill=(255,255,0,255))

    #write tasks
    for i in range(len(tasks)):
        draw.text((midx+txt_margin,pos[i]), tasks[i]["message"], font=fnt, fill=(255,255,255,255))

    out = Image.alpha_composite(wallpaper, txt)
    return out

#sample tasks
tasks = []
for i in range(10):
    tasks.append({"message":f'Task {i+1}',"urg/imp":round(random.uniform(0,1),2)})
tasks = sorted(tasks,key = lambda t: t["urg/imp"])
pprint.pprint(tasks)

#get the wallpaper image in RGBA format
wallpaper = Image.open(get_wallpaper()).convert('RGBA')

wallpaper.save('original.png')

new_wallpaper = set_up(wallpaper,tasks)

new_wallpaper.save('modified.png')
