#!/usr/bin/python3

"""
A command line to-do list for linux.

This module handles the input from the user and relies on
to_do_list_tasks.py for the manipulation of the tasks.

for more information run: ./to_do_list --help
"""

import argparse
import sys
import datetime
from to_do_list_tasks import tasks


# add command line arguement parsing
parser = argparse.ArgumentParser()
parser.add_argument(
    '-v', '--verbose', help='output additional text to tell you what was done', action='store_true')
parser.add_argument(
    '-a', '--add', help='add a new task to your to-do list', action='store_true')
parser.add_argument('-f', '--find', help='search your to-do list')
parser.add_argument(
    '-s', '--show', help='display your entire to-do list', action='store_true')
parser.add_argument(
    '--sortBy', help='sort your to-do list. Options are - date, urg, imp, default. leave empty for default',
                   choices=['date', 'urg', 'imp', 'default'], nargs='?', const='default')
parser.add_argument(
    '--mark', help='mark a task as "Done"', action='store_true')
parser.add_argument(
    '--remove', help='remove your entire list', action='store_true')
parser.add_argument(
    '--save', help='save to-do list to a custom file', default='to-do-list-data.json')
parser.add_argument(
    '--load', help='load to-do list from a custom file', default='to-do-list-data.json')
parser.add_argument('-w', '--wallpaper',
                    help='update wallpaper based on your current list', action='store_true')
parser.add_argument(
    '--audioPath', help='update reminder audio', default='./default_audio.mp3')


def menu(to_do_list):

    """handle input given by user in the form of arguements"""

    # load from file (default if nothing is specified)
    if arg.verbose:
        print('[ loading from {} ]'.format(arg.load))
    try:
        to_do_list.load(arg.load)
    except FileNotFoundError:
        print('You haven\'t saved any tasks in {} Yet!'.format(arg.load))

    # display help if no arguements are given
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # add a new message to the to-do list
    if arg.add:
        if arg.verbose:
            print('[ add a new task to your to-do list ]')

        message = input('Message: ')

        correct_date = False
        while not correct_date:
            try:
                date = input('Due date(DD-MM-YYYY): ')
                day, month, year = date.split('-')
                date = datetime.date(int(year), int(month), int(day))
                correct_date = True
            except Exception as e:
                print('{}! Please try again!'.format(e))

        urg = int(input('How urgent is this task(1-10): '))
        while urg not in range(1, 10 + 1):
            print('Out of bounds! Try Again')
            urg = int(input('How urgent is this task(1-10): '))

        imp = int(input('How important is this task(1-10): '))
        while imp not in range(1, 10 + 1):
            print('Out of bounds! Try Again')
            imp = int(input('How important is this task(1-10): '))

        # add task to to do list
        to_do_list.add(message, date, urg, imp)

    # find tasks that contain arguement of --find
    if arg.find:
        if arg.verbose:
            print('[ Looking for {} ]'.format(arg.find))
        search_results = to_do_list.search(arg.find)
        to_do_list.show(full_list=False, partial_list=search_results)

    if arg.show:
        if arg.verbose:
            print('[ your to-do list: ]')
        to_do_list.show()

    if arg.sortBy:
        if arg.verbose:
            print('[ sort using {} ]'.format(arg.sortBy))
        if arg.sortBy == 'default':
            to_do_list.sort()
        else:
            to_do_list.sort(arg.sortBy)

    if arg.mark:
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
        to_do_list.update_wallpaper()

    if arg.remove:
        if input('Are You sure you want to clear your entire list? (y/n): ').lower() == 'y':
            to_do_list.empty()

    if arg.wallpaper:
        path = to_do_list.update_wallpaper()
        if arg.verbose:
            print(
                '[ You may need to restart gnome for the changes to be reflected ]')
            print('[ new wallpaper is stored at {} ]'.format(path))
            print('[ original wallpaper is stored at {} ]'.format(
                to_do_list.get_wallpaper()))

    if arg.audioPath:
        if arg.verbose:
            print('[ path for audio file is {} ]'.format(arg.audioPath))
        path = arg.audioPath
        while not to_do_list.reminder_audio(path):
            path = input('Enter path of Audio File: ')

    if arg.verbose:
        print('[ saving to {} ]'.format(arg.save))
    to_do_list.save()


if __name__ == '__main__':

    # initialize to-do list
    to_do_list = tasks()

    arg = parser.parse_args()

    #user options for list
    menu(to_do_list)
