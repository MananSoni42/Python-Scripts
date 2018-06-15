#pip install python-vlc
import datetime
import vlc
import os
import time





def checkTasks():
	list2 = [item[1] for task in finalList]
	now = datetime.datetime.now()
	today = now.strftime('%Y-%m-%d')
	flag = 0

#if the due date matches today's date play the audio if not notify
#No task for that day
	for date in list2:
		if date == today:
			flag =1
			p = vlc.MediaPlayer("default_audio")
		        p.play()
	if flag == 0:
		os.system(' notify-send "No task for today" ')

if __name__ == '__main__' :
	checkTasks()
	
	
