import praw
import SubredditWatcher

class SubredditWatcherHandler:

    def __init__(self, username, password, triggers, subreddits, user_agent):
        self.subreddits = subreddits
        self.triggers = triggers
		
        # Setup reddit api object
        self.praw_reddit = praw.Reddit(user_agent=user_agent)
        self.praw_reddit.login(username, password)

        self.subredditWatchers = []
        for subreddit_name in subreddits:
            self.subredditWatchers.append(SubredditWatcher(subreddit_name), self.praw_reddit, triggers)

    def processSubreddits(self):
        for watcher in self.subredditWatchers:
            watcher.watch()
