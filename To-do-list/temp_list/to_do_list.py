import json
import os
import datetime
from PIL import Image,ImageDraw,ImageFont
from gi.repository import Gio
#from playsound import playsound
from pygame import mixer

class tasks:
    tasks = []
    default_audio = './consequence.mp3'
    def add(self,message,date,urg,imp):
        task = {}
        task["message"] = message
        task["date"] = date
        task["urg"] = urg
        task["imp"] = imp
        urg_imp = round(urg/imp,2)
        task["urg/imp"] = urg_imp
        task["done"] = False
        self.tasks.append(task)

    def show(self,full_list=True,partial_list=None,num=False):
        if full_list:
            t = self.tasks
        else:
            t = partial_list

        if num:
            count = 1
            for task in t:
                print(f'{count} - {task["message"]} - {task["date"]} - urg: {task["urg"]} - imp: {task["imp"]}')
                count+=1
                print(' ')
        else:
            for task in t:
                print(f'{task["message"]} - {task["date"]} - urg: {task["urg"]} - imp: {task["imp"]}')
                print(' ')
        return len(t)

    def empty(self):
        self.tasks = []

    def sort(self,user_key=None):
        if not user_key:
            k = lambda x: (x['urg'],x['imp'])
        else:
            k = lambda x: x[user_key]
        self.tasks.sort(key = k,reverse=True)

    def search(self,key,value):
        t = []
        for task in self.tasks:
            if task[key] == value:
                t.append(task)
        return t

    def keyword_search(self,keyword):
        t = []
        for task in self.tasks:
            if keyword in task["message"]:
                t.append(task)
        return t

    def save(self,out_file='to-do-list-data.json'):
        print(f'saving to {out_file}')
        data = {"to-do-list":self.tasks,"audio":self.default_audio}
        with open(out_file,'w') as f:
            json.dump(data,f,indent = 4,default=str)

    def load(self,in_file ='to-do-list-data.json'):
        print(f'loading from {in_file}')

        self.upcoming_reminders()
        self.current_reminders()

        with open(in_file) as f:
            self.tasks = json.load(f)["to-do-list"]
            self.default_audio = json.load(f)["audio"]
            for task in self.tasks:
                date = task["date"]
                year,month,day = date.split('-')
                task["date"] = datetime.date(int(year),int(month),int(day))
    #returns the path to the current wallpaper
    #utility for update_wallpaper
    def get_wallpaper(self):
        settings = Gio.Settings.new("org.gnome.desktop.background")
        uri = settings.get_string("picture-uri")

        if 'file' in uri:
            path =  uri.strip('file')[3:]
        else:
            with open('orig_wallpaper.txt') as f:
                path = f.read()

        with open('orig_wallpaper.txt','w') as f:
            f.write(str(path))

        return path

    #update wallpaper to given wallpaper
    def update_wallpaper(self):
        tasks = self.tasks
        final_img = self.make_img_from_list()
        final_img.save('final.png')
        path = os.getcwd() + '/final.png'
        os.system(f'/usr/bin/gsettings set org.gnome.desktop.background picture-uri {path}')
        #os.system('/usr/bin/gsettings set org.gnome.desktop.background picture-uri /home/manan/acm/summers-SIG-2018/Python-Scripts/To-do-list/final.png')

    #sets up the tasks on the current wallpaper
    #utility for update_wallpaper
    def set_up(self,wallpaper):
        tasks = self.tasks
        midx = int(round(wallpaper.size[0]/2,0))
        num = len(tasks)
        height = wallpaper.size[1]
        margin = 50
        txt_margin = 20

        #positions of all messages
        #leave one extra empty space (if last message is very long)
        pos = [i*height/(num+1) for i in range(num+1)]
        last = pos[-1]
        pos = [p + (height-last)/2 for p in pos]

        # make a blank image for the text, initialized to transparent text color
        txt = Image.new('RGBA', wallpaper.size, (255,255,255,0))
        # get a font
        fnt = ImageFont.truetype('Pillow/Tests/fonts/DejaVuSans.ttf', 50)
        f1_size = 75
        fnt1 = ImageFont.truetype('Pillow/Tests/fonts/DejaVuSans.ttf', f1_size)
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
                    #cut text if it is 'done'
                    if tasks[i]["done"] is True:
                        draw.line((midx+txt_margin,pos[i]+c*count+fnt.getsize(tasks[i]["message"])[1]/2,midx+txt_margin+fnt.getsize(' '.join(lst[:lst.index(l)-1]))[0],pos[i]+c*count+fnt.getsize(tasks[i]["message"])[1]/2),width=6,fill="white")
                    #write the chosen text
                    draw.text((midx+txt_margin,pos[i]+c*count), ' '.join(lst[:end]), font=fnt, fill=(255,255,255,255))
                    #delete text that has been written and continue
                    del lst[:end]
                    count+=1
            #only one line for this task
            else:
                #cut text if it is 'done'
                if tasks[i]["done"] is True:
                    draw.line((midx+txt_margin,pos[i]+fnt.getsize(tasks[i]["message"])[1]/2,midx+txt_margin+fnt.getsize(tasks[i]["message"])[0],pos[i]+fnt.getsize(tasks[i]["message"])[1]/2),width=6,fill="white")
                draw.text((midx+txt_margin,pos[i]), tasks[i]["message"], font=fnt, fill=(255,255,255,255))

        out = Image.alpha_composite(wallpaper, txt)
        return out

    #utility for update_wallpaper
    def make_img_from_list(self):
        tasks = self.tasks
        #get the wallpaper image in RGBA format
        wallpaper = Image.open(self.get_wallpaper()).convert('RGBA')

        #add to-do list on top of the wallpaper
        new_wallpaper = self.set_up(wallpaper)

        return new_wallpaper

    #reminders for tomorrow
    def upcoming_reminders(self):
        tom_tasks = [ task for task in self.tasks if task["date"] == datetime.date.today() + datetime.timedelta(days=1)  ]
        if not tom_tasks:
            os.system('notify-send "No tasks for tomorrow!" ')
        else:
            for task in tom_tasks:
                os.system(f'notify-send "Upcoming: {task["message"]}" ')

    #utility for current reminders
    def ask_user(self,today_tasks):
        for task in today_tasks:
            ans = input(f'have you completed {task["message"]} (y/n)?: ').lower()
            ind = self.tasks.index(task)
            if ans == 'y':
                self.tasks[ind]["done"] = True
            if ans == 'n':
                val = input(f'would you like to:\n1: delete task\n2: change due date\n')
                if val is '1':
                    del self.tasks[ind]
                if val is '2':
                    date = input('Due Date(dd-mm-yyyy): ')
                    day,month,year = date.split('-')
                    date = datetime.date(int(year),int(month),int(day))
                    self.tasks[ind]["date"] = date

    #reminders for today
    def current_reminders(self):
        today_tasks = [ task for task in self.tasks if task["date"] == datetime.date.today() ]
        if not today_tasks:
            os.system('notify-send "No tasks for Today!" ')
        else:
            for task in today_tasks:
                os.system(f'notify-send "Due today: {task["message"]}" ')
            mixer.init()
            mixer.music.load(self.default_audio)
            mixer.music.play()
            self.ask_user(today_tasks)

    def mark_as_done(self,val):
        ind = int(val) - 1
        print(f'marked "{self.tasks[ind]["message"]}" as Done')
        self.tasks[ind]["done"] = True

    #cahnge default audio to user supplied Audio
    def reminder_audio(path):
        if not os.path.isfile(path):
            print('No such file exists')
            return False
        if os.path.splitext(path)[1].lower() not in ['.mp4','.wav']:
            print('Incorrect Format! Only .mp3 and .wav files are supported')
            return False
        else:
            self.default_audio = path
            return True
