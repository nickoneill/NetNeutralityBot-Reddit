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

from modules.account import credentials
from prawcore.exceptions import Forbidden


class PostHandler:

    # Edit subreddits here. Keep in mind, we probably shouldn't include subreddits like
    # /r/NetNeutrality, since they probably already know this information.
    subreddits = ['technology', 'all']
    search_terms = ['net neutrality']

    @staticmethod
    def find_matches(reddit, database):
        print('Finding posts that contain "Net Neutrality"')
        matches = []
        for subreddit in PostHandler.subreddits:
            posts = reddit.get_submissions(subreddit)
            for post in posts:
                for term in PostHandler.search_terms:
                    if term in post.title.lower() or (post.link_flair_text and term in post.link_flair_text.lower()):
                        if not database.match_exists(post.permalink):
                            matches.append((term, post))
        return matches

    @staticmethod
    def handle_matches(reddit, database, matches, message):
        for term, post in matches:
            try:
                database.insert_comment(post.permalink)
                comment = post.reply(message)
                database.commit()
                reddit.send_message(
                    credentials['developer'],
                    'NetNeutralityBot - Posted',
                    'NetNeutralityBot - Posted\n\t \n' +
                    '[' + str(post.title) + '](' + comment.permalink + ')'
                )
            except Forbidden as e:
                database.commit()  # Commit entry for subreddit posts where bot is banned
                print('Forbidden')
