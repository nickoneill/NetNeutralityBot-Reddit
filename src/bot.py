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

GITHUB_HOME = ''
GITHUB_README = ''


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
                print(traceback.format_exc())
                self.database.reset()
                self.reddit.reset()
                self.reddit.send_message(credentials['developer', 'NetNeutralityBot crashed'], traceback.format_exc())
            time.sleep(20)

    def read_file(self):
        with open(os.path.join(ROOT_DIR, 'resources/message.txt'), 'r') as messageFile:
            self.message = messageFile.read().replace('\n', '') + self.signature()
            print('MESSAGE:\n' + self.message)
            time.sleep(5)

    def signature(self):
        signature = \
            '\n\t \n\t \n-/u/' + credentials['username'] + '\n\t \n\t \n' + \
            '/u/' + credentials['developer'] + ' | ' + \
            '[Bot Code](' + GITHUB_HOME + ')\n' + \
            '[Readme](' + GITHUB_README + ')\n'
        return signature


bot = NetNeutralityBot()
bot.start()
