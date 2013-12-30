#!/usr/bin/env python
import codecs
import time
import praw
import util
from SubredditWatcherHandler import SubredditWatcherHandler
from MentionsWatcher import MentionsWatcher
from ConfigParser import SafeConfigParser

def main():
    util.bot_stdout_print("Script started.")

    # Parse config file
    parser = SafeConfigParser()
    with codecs.open("bot.ini", "r", encoding="utf-8") as f:
        parser.readfp(f)
    url = parser.get("General", "url")
    summary = parser.get("General", "summary")
    username = parser.get("General", "reddit_username")
    password = parser.get("General", "reddit_password")
    triggers = tuple(parser.get("General", "subreddit_triggers").split(","))
    subreddits = tuple(parser.get("General", "subreddits").split(","))
    user_agent = "%s %s" % (summary, url)

    # Setup reddit api object and login
    praw_reddit = praw.Reddit(user_agent=user_agent)
    praw_reddit.login(username, password)

    # Setup the subreddit watcher handler
    watcher_handler = SubredditWatcherHandler(praw_reddit, username, triggers, subreddits)

    # Setup the mentions watcher
    mentions_watcher = MentionsWatcher(praw_reddit, username)

    # Main loop
    while True:
        util.bot_stdout_print("Main loop started.")
        watcher_handler.process_subreddits()
        mentions_watcher.watch()
        util.bot_stdout_print("Sleeping for 3 seconds.")
        time.sleep(3)

if __name__ == "__main__":
    main()
