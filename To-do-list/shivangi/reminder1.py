#pip install pygame
from datetime import date
from pygame import mixer
import subprocess
import os
import time





def checkTasks():
	list2 = [item[1] for task in finalList]
	today = date.today()
	flag = 0
	for date in list2:
		if date == today:
			flag =1
			pygame.mixer.init()
			pygame.mixer.music.load(default_audio)
			pygame.mixer.music.play()
	if flag == 0:
		os.system(' notify-send "No task for today" ')

if __name__ == '__main__' :
	checkTasks()
