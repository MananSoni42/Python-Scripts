#pip install playsound

import create_list
import os
import subprocess
from datetime import date
from playsound import playsound

def checkTasks():
  list2 = [item[1] for task in finalList]
  print(list2)
  print(finalList)
  today = date.today()
  flag = 0
  for date in list2:
    if date == today:
      flag = 1
      playsound(default_audio)
      #os.system(f'notify-send "{tas}" ')
  if flag == 0:
    os.system('notify-send "No task for today" ')

if __name__ == '__main__':
  checkTasks()
