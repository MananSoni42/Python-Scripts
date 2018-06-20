""" to be run each time a user starts his computer """

from to_do_list_tasks import tasks

if __name__ == '__main__':

    to_do_list = tasks()
    to_do_list.load(notif=True)
    to_do_list.update_wallpaper()
