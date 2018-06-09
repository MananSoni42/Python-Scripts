import random
from PIL import Image,ImageDraw,ImageFont
from gi.repository import Gio
import pprint

#returns the path to the current wallpaper
def get_wallpaper():
    settings = Gio.Settings.new("org.gnome.desktop.background")
    uri = settings.get_string("picture-uri")
    return uri.strip('file')[3:]

def set_up(wallpaper,tasks):

    midx = int(round(wallpaper.size[0]/2,0))
    num = len(tasks)
    height = wallpaper.size[1]
    margin = 50
    txt_margin = 20

    #positions of all messages
    #leave one extra empty space (if last message is very long)
    pos = [i*height/num for i in range(num+1)]
    last = pos[-1]
    del pos[-1]
    pos = [p + (height-last)/2 for p in pos]
    #print(pos1)

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
        #text goes beyond ending - wrap text
        if midx + txt_margin + fnt.getsize(tasks[i]["message"])[0] > wallpaper.size[0] - margin:
            l = len(tasks[i]["message"])
            c = fnt.getsize(tasks[i]["message"])[1]
            lst = tasks[i]["message"].split(' ')
            count = 0
            #break text into smaller pieces to fit in screen
            #until list with words is not empty
            while lst != []:
                end = len(lst)
                for l in lst:
                    if midx + txt_margin + fnt.getsize(' '.join(lst[:lst.index(l)]))[0] > wallpaper.size[0] - margin:
                        end = lst.index(l)-1
                        break
                #write the chosen text
                draw.text((midx+txt_margin,pos[i]+c*count), ' '.join(lst[:end]), font=fnt, fill=(255,255,255,255))
                #delete text that has been written and continue
                del lst[:end]
                count+=1

#            draw.text((midx+txt_margin,pos[i]), tasks[i]["message"][:int(l/3)], font=fnt, fill=(255,255,255,255))
#            draw.text((midx+txt_margin,pos[i]+c), tasks[i]["message"][int(l/3):int(2*l/3)], font=fnt, fill=(255,255,255,255))
#            draw.text((midx+txt_margin,pos[i]+2*c), tasks[i]["message"][int(2*l/3):], font=fnt, fill=(255,255,255,255))

        else:
            draw.text((midx+txt_margin,pos[i]), tasks[i]["message"], font=fnt, fill=(255,255,255,255))

    out = Image.alpha_composite(wallpaper, txt)
    return out

def make_img_from_list(tasks):
    #get the wallpaper image in RGBA format
    wallpaper = Image.open(get_wallpaper()).convert('RGBA')

    #add to-do list on top of the wallpaper
    new_wallpaper = set_up(wallpaper,tasks)

    return new_wallpaper


if __name__ == '__main__':

    #sample tasks
    tasks = []
    for i in range(10):
        if i is 4:
            tasks.append({"message":f'Task {i+1} this is a very very very long message used to test whether text wrapping is working correctly or not. aaaaaaaaaa bbbbbbbbbbbb cccccccccccc ddddddddddd',"urg/imp":round(random.uniform(0,1),2)})
        else:
            tasks.append({"message":f'Task {i+1}',"urg/imp":round(random.uniform(0,1),2)})

    tasks = sorted(tasks,key = lambda t: t["urg/imp"])
    pprint.pprint(tasks)

    final_img = make_img_from_list(tasks)

    final_img.save('final.png')
