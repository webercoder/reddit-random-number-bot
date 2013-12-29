import reddit

class MentionsWatcher:

    def __init__(self, praw_reddit):
        self.praw_reddit = praw_reddit
        self.username = username

    def watch(self):
        mentions = self.praw_reddit.get_mentions()
        