#!/usr/bin/env python
import codecs
import time
from SubredditWatcherHandler import SubredditWatcherHandler
from ConfigParser import SafeConfigParser

def main():
    # Parse config file
    parser = SafeConfigParser()
    with codecs.open("bot.ini", "r", encoding="utf-8") as f:
        parser.readfp(f)
    url = parser.get("General", "url")
    summary = parser.get("General", "summary")
    username = parser.get("General", "reddit_username")
    password = parser.get("General", "reddit_password")
    triggers = tuple(parser.get("General", "triggers").split(","))
    subreddits = tuple(parser.get("General", "subreddits").split(","))
    user_agent = "%s %s" % (summary, url)

    # Setup the subreddit watcher handler
    watcher_handler = SubredditWatcherHandler(username, password, triggers, subreddits, user_agent);

    # Main loop
    while True:
        watcher_handler.process_subreddits()
        time.sleep(5)

if __name__ == "__main__":
    main()