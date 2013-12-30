from SubredditWatcher import SubredditWatcher

class SubredditWatcherHandler:

    def __init__(self, praw_reddit, username, triggers, subreddits):
        self.subreddits = subreddits
        self.triggers = triggers
        self.subreddit_watchers = []
        for subreddit_name in subreddits:
            self.subreddit_watchers.append(SubredditWatcher(subreddit_name, praw_reddit, triggers, username))

    def process_subreddits(self):
        for watcher in self.subreddit_watchers:
            watcher.watch()
