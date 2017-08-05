"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        NetNeutralityBot
Date Created:       08/04/2017
Date Last Edited:   08/04/2017
Version:            v1.0
==========================================
"""

import time
from modules.account import credentials


def handle_crash(stacktrace, reddit=None, database=None):
    reset = False
    while not reset:
        time.sleep(30)
        try:
            print('Trying to handle error \n\n' + stacktrace)
            if reddit:
                reddit.reset()
            if database:
                database.reset()
            reddit.send_message(credentials['developer'], credentials['username'] + ' - Exception Handled', stacktrace)
            reset = True
        except:
            print('Failed to restart bot. Trying again in 30 seconds.')
