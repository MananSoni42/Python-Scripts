from to_do_list import tasks
import datetime

#menu for user
def menu(to_do_list):

    while True:
        print('''
        ------- TO DO LIST -------
        1 - Add a task
        2 - search for a task
        3 - mark a task as 'Done'
        4 - sort tasks by Due Date
        5 - Show all tasks
        6 - empty list
        7 - save list to file
        8 - load list from file
        9 - update wallpaper
        10 - change reminder audio
        11 - exit
        ''')

        correct_val = False
        while correct_val is False:
            try:
                val = int(input('\n>>> '))
                correct_val = True
            except ValueError:
                print('Incorrect option, Try again!')

        if val not in range(1,11+1):
            val = input('Incorrect Choice! Enter again: ')

        if val == 1:

            #input message
            message = input('Message: ')
            correct_date = False

            #input date
            while not correct_date:
                try:
                    date = input('Due date(DD-MM-YYYY): ')
                    day, month, year = date.split('-')
                    date = datetime.date(int(year), int(month), int(day))
                    correct_date = True
                except Exception as e:
                    print(f'{e}! Please try again!')

            #input priority
            urg = int(input('How urgent is this task(1-10): '))
            while urg not in range(1,10+1):
                print('Out of bounds! Try Again')
                urg = int(input('How urgent is this task(1-10): '))

            imp = int(input('How important is this task(1-10): '))
            while imp not in range(1,10+1):
                print('Out of bounds! Try Again')

                imp = int(input('How important is this task(1-10): '))

            print(' ')
            #add task to to do list
            to_do_list.add(message,date,urg,imp)

        if val == 2:
            print('''
            search by:
            1 - Message
            2 - keyword
            3 - date
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
                    #try:
                    print('Due date(DD-MM-YYYY): ',end=' ')
                    date = input()
                    day, month, year = date.split('-')
                    date = datetime.date(int(year), int(month), int(day))
                    correct_date = True
                    #except Exception as e:
                print('')

                plist = to_do_list.search(key='date',value=date)

            print('\n\t[\n\n  Search Results:\n')
            to_do_list.show(full_list=False,partial_list=plist)
            print('\n\t]\n')

        if val == 3:
            tlen = to_do_list.show(num=True)
            tval_correct = False

            while tval_correct is False:
                try:
                    tval = int(input("Enter index of Task: "))
                    while tval not in range(1,tlen+1):
                        tval = int(input(f'Out of bounds, Enter a value between 1 and {tlen+1}: '))
                    tval_correct = True
                except ValueError:
                    print('An Integer is required! Please try again')
            to_do_list.mark_as_done(tval)
            to_do_list.update_wallpaper

        if val == 4:
            to_do_list.sort('date')

        if val == 5:
            print('\n\t[\n\n Your to-do list:\n')
            to_do_list.show()
            print('\t]\n')

        if val == 6:
            to_do_list.empty()

        if val == 7:
            to_do_list.save()

        if val == 8:
            try:
                to_do_list.load()
            except FileNotFoundError:
                print('You haven\'t saved any tasks Yet!')

        if val == 9:
            print('You may need to restart gnome for the changes to be reflected!')
            to_do_list.update_wallpaper()

        if val == 10:
            path = input('Enter path of Audio File: ')
            while not to_do_list.reminder_audio(path):
                path = input('Enter path of Audio File: ')

        if val == 11:
            to_do_list.save()
            break
        print('')

### --- MAIN --- ###

to_do_list = tasks()

menu(to_do_list)
