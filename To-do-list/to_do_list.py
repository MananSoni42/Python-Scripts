import json
import datetime

class tasks:
    tasks = []
    def add(self,message,date,urg_imp):
        task = {}
        task["message"] = message
        task["date"] = date
        task["urg/imp"] = urg_imp
        task["done"] = False
        self.tasks.append(task)

    def show(self,full_list=True,partial_list=None):
        if full_list:
            t = self.tasks
        else:
            t = partial_list
        for task in t:
            for key,value in task.items():
                print(f'{key}: {value}')
            print(' ')

    def empty(self):
        self.tasks = []

    def sort(self,key="urg/imp"):
        k = lambda x: x[key]
        self.tasks = sorted(self.tasks,key = k)

    def search(self,key,value):
        t = []
        for task in self.tasks:
            if task[key] == value:
                t.append(task)
        return t

    def keyword_search(self,keyword):
        t = []
        for task in tasks:
            if keyword in task["message"]:
                t.append(task)
        return t

    def save(self,out_file='to-do-list-data.json'):
        data = {"to-do-list":self.tasks}
        with open(out_file,'w') as f:
            json.dump(data,f,indent = 4)

    def load(self,in_file ='to-do-list-data.json'):
        with open(in_file) as f:
            self.tasks = json.load(f)["to-do-list"]

#menu for user
def menu(to_do_list):
    print('''
    ------- TO DO LIST -------
    1 - Add a task
    2 - search for a task
    3 - Show all tasks
    4 - empty list
    5 - save list from file
    6 - load list from file
    7 - exit
    ''')
    val = int(input('\n>>> '))
    while val != 7:
        if val not in range(1,7+1):
            val = input('Incorrect Choice! Enter again: ')

        if val == 1:

            #input message
            message = input('Message: ')
            print('')
            correct_date = False

            #input date
            while not correct_date:
                try:
                    date   = input('Due date(DD-MM-YYYY): ')
                    day, month,year = date.split('-')
                    date = datetime.date(year, month, day)
                    correct_date = True
                except Exception as e:
                    print(f'{e}! PLease try again!')
            print('')

            #input priority
            urg = int(input('How urgent is this task(1-10): '))
            while urg not in range(1,10+1):
                print('Out of bounds! Try Again')
                urg = int(input('How urgent is this task(1-10): '))

            imp = int(input('How important is this task(1-10): '))
            while imp not in range(1,10+1):
                print('Out of bounds! Try Again')
                imp = int(input('How important is this task(1-10): '))
            urg_imp = round(urg/imp,2)
            print(' ')
            #add task to to do list
            to_do_list.add(message,date,urg_imp)

        if val == 2:
            print('''
            search by:
            1 - Message
            3 - keyword
            2 - date
            ''')
            sval = int(input('\n> '))
            while sval not in [1,2,3]:
                sval = input('Incorrect Choice! Enter again: ')

            if sval == 1:
                message = input('Message to be searched: ')
                plist = to_do_list.search(key='message',value=message)

            if sval == 2:
                keyword = input('Enter keyword to be searched: ')
                plist = to_do_list.keyword_search(keyword)

            if sval == 3:
                #input date
                correct_date = False
                while not correct_date:
                    try:
                        date   = input('Due date(DD-MM-YYYY): ')
                        day, month,year = date.split('-')
                        date = datetime.date(year, month, day)
                        correct_date = True
                    except Exception as e:
                        print(f'{e}! PLease try again!')
                print('')

                plist = to_do_list.search(key='date',value=date)

            print('\n---> Search Results:\n')
            to_do_list.show(full_list=False,partial_list=plist)

        if val == 3:
            print('\n---> Your to-do list:\n')
            to_do_list.show()

        if val == 4:
            to_do_list.emptyList()

        if val == 5:
            to_do_list.save()

        if val == 6:
            to_do_list.load()

        if val == 7:
            break

        print('''
        ------- TO DO LIST -------
        1 - Add a task
        2 - search for a task
        3 - Show all tasks
        4 - empty list
        5 - save list from file
        6 - load list from file
        7 - exit
        ''')
        val = int(input('\n>>> '))

### --- MAIN --- ###

to_do_list = tasks()
menu(to_do_list)
