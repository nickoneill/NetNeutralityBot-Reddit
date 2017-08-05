"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        NetNeutralityBot
Date Created:       08/03/2017
Date Last Edited:   08/03/2017
Version:            v1.0
==========================================
"""

import os
import time
import traceback

from src.definitions import ROOT_DIR
from src.modules.account import credentials
from src.modules.database_handler import DatabaseHandler
from src.modules.post_handler import PostHandler
from src.modules.reddit_handler import RedditHandler
from src.modules.crash_handler import handle_crash


GITHUB_HOME = 'https://github.com/tylerbrockett/NetNeutralityBot-Reddit'
GITHUB_README = 'https://github.com/tylerbrockett/NetNeutralityBot-Reddit/blob/master/README.md'


class NetNeutralityBot:

    def __init__(self):
        self.reddit = RedditHandler(credentials)
        self.database = DatabaseHandler(os.path.join(ROOT_DIR, 'database/data.db'))
        self.message = ''
        self.read_file()

    def start(self):
        while True:
            try:
                posts = PostHandler.find_matches(self.reddit, self.database)
                print(str(len(posts)) + ' matches found')
                PostHandler.handle_matches(self.reddit, self.database, posts, self.message)
            except:
                handle_crash(traceback.format_exc(), self.reddit, self.database)
            time.sleep(20)

    def read_file(self):
        with open(os.path.join(ROOT_DIR, 'resources/message.txt'), 'r') as messageFile:
            self.message = messageFile.read() + self.signature()
            print('MESSAGE:\n' + self.message)
            time.sleep(5)

    def signature(self):
        signature = \
            '\n\t \n\t \n-/u/' + credentials['username'] + '\n\t \n\t \n' + \
            '[Contact Developer](/u/' + credentials['developer'] + ') | ' + \
            '[Bot Code](' + GITHUB_HOME + ') | ' + \
            '[Readme](' + GITHUB_README + ')\n'
        return signature


bot = NetNeutralityBot()
bot.start()
