import praw
from SubredditWatcher import SubredditWatcher

class SubredditWatcherHandler:

    def __init__(self, username, password, triggers, subreddits, user_agent):
        self.subreddits = subreddits
        self.triggers = triggers
		
        # Setup reddit api object
        self.praw_reddit = praw.Reddit(user_agent=user_agent)
        self.praw_reddit.login(username, password)

        self.subreddit_watchers = []
        for subreddit_name in subreddits:
            self.subreddit_watchers.append(SubredditWatcher(subreddit_name, self.praw_reddit, triggers, username))

    def process_subreddits(self):
        for watcher in self.subreddit_watchers:
            watcher.watch()
