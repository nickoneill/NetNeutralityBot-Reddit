"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        NetNeutralityBot
Date Created:       08/06/2017
Date Last Edited:   08/06/2017
Version:            v1.0
==========================================
"""

from modules.account import credentials


class InboxHandler:

    @staticmethod
    def handle_stats_message(message, count):
        message.reply('Bot has responded to ' + str(count) + ' posts.')
        message.mark_read()

    @staticmethod
    def handle_comment_reply(message, reddit):
        reddit.send_message(
            credentials['developer'],
            'NetNeutralityBot - Comment Reply',
            '[Comment Reply](' + message.permalink + ')\t\n \t\n' +
            'Username: /u/' + str(message.author) + '\t\n \t\n' +
            'Body:        ' + str(message.body)
        )

    @staticmethod
    def handle_default_message(reddit, message):
        reddit.send_message(
            credentials['developer'],
            'NetNeutralityBot - Message',
            'Username: /u/' + str(message.author) + '\t\n \t\n' +
            'Subject:     ' + str(message.subject) + '\t\n \t\n' +
            'Body:        ' + str(message.body)
        )
        message.mark_read()

    @staticmethod
    def read_inbox(database, reddit):
        print('Reading inbox...')
        unread = reddit.get_unread()
        for message in unread:
            subject = str(message.subject).lower()
            if subject in ['stats', 'statistics']:
                count = database.count_posts()
                InboxHandler.handle_stats_message(message, count)
            elif subject in ['comment reply']:
                InboxHandler.handle_comment_reply(message, reddit)
            else:
                InboxHandler.handle_default_message(reddit, message)
