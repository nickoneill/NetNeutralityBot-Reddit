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

import traceback
import praw


class RedditHandler:

    def __init__(self, credentials):
        self.credentials = credentials
        self.reddit = self.connect()
        self.NUM_POSTS = 20

    def connect(self):
        try:
            reddit = praw.Reddit(
                client_id=self.credentials['client_id'],
                client_secret=self.credentials['client_secret'],
                password=self.credentials['password'],
                user_agent=self.credentials['user_agent'],
                username=self.credentials['username'])
            return reddit
        except:
            raise RedditHelperException('Error connecting to Reddit\n\n' + traceback.format_exc())

    def disconnect(self):
        self.reddit = None

    def reset(self):
        try:
            self.disconnect()
            self.reddit = self.connect()
        except:
            raise RedditHelperException(RedditHelperException.RESET_EXCEPTION + '\n\n' + traceback.format_exc())

    def send_message(self, redditor, subject, body):
        try:
            self.reddit.redditor(redditor).message(subject, body)
        except:
            print(traceback.format_exc())
            raise RedditHelperException(RedditHelperException.SEND_MESSAGE_EXCEPTION)

    def get_unread(self):
        try:
            ret = []
            unread = self.reddit.inbox.unread(limit=None)
            for message in unread:
                ret.append(message)
            ret.reverse()
            return ret
        except:
            return []

    def get_submissions(self, subreddit):
        submissions = []
        posts = 200 if (subreddit == 'all') else self.NUM_POSTS
        try:
            if subreddit == 'all':
                submissions = self.reddit.subreddit(subreddit).hot(limit=posts)
            else:
                submissions = self.reddit.subreddit(subreddit).new(limit=posts)
        except:
            print(traceback.format_exc())
            raise RedditHelperException(RedditHelperException.GET_SUBMISSIONS_EXCEPTION)
        return submissions


class RedditHelperException(Exception):
    SEND_MESSAGE_EXCEPTION = 'Error sending message'
    RESET_EXCEPTION = 'Error resetting connection to Reddit'
    GET_SUBMISSIONS_EXCEPTION = 'Error getting submissions'

    def __init__(self, error_args):
        Exception.__init__(self, 'Reddit Exception: {0}'.format(error_args))
        self.errorArgs = error_args
