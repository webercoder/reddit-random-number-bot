from SubredditWatcher import SubredditWatcher
import time

class SubredditWatcherHandler:

    DELAY = 2 # seconds

    def __init__(self, praw_reddit, username, triggers, subreddits):
        self.subreddits = subreddits
        self.triggers = triggers
        self.subreddit_watchers = []
        self.last_run = None
        for subreddit_name in subreddits:
            self.subreddit_watchers.append(SubredditWatcher(subreddit_name, praw_reddit, triggers, username))

    def process_subreddits(self):
        now = int(time.time())
        if self.last_run is None or now - self.last_run > self.DELAY:
            for watcher in self.subreddit_watchers:
                watcher.watch()
            self.last_run = int(time.time())