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
    def handle_comment_reply(comment, reddit):
        comment.mark_read()
        if 'good bot' in comment.body.lower():
            comment.reply('Good human.')
        reddit.send_message(
            credentials['developer'],
            'NetNeutralityBot - Comment Reply',
            '[Comment Reply](' + comment.context + ')\t \n' +
            '**Username:** /u/' + comment.author.name + '\t \n' +
            '**Body:**\t \n' + comment.body
        )

    @staticmethod
    def handle_default_message(message, reddit):
        reddit.send_message(
            credentials['developer'],
            'NetNeutralityBot - Message',
            'Username: /u/' + message.author.name + '\t \n' +
            'Subject:     ' + message.subject + '\t \n' +
            'Body:        ' + message.body
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
            elif message.was_comment:
                InboxHandler.handle_comment_reply(message, reddit)
            else:
                InboxHandler.handle_default_message(message, reddit)
