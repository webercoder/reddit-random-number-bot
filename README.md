# Reddit Random Number Bot

## Summary

This bot creates random numbers from two given integers. It responds in two ways:

* Subreddit Triggers
* Reddit-Wide Mentions (the bot must have an active Reddit gold subscription)

**Subreddit Triggers** work by posting a comment in a watched subreddit. When a trigger word starts a line in the comment, it will be picked up by the bot. Syntax:

    triggerword low high

**Reddit-Wide Mentions** work by posting a comment anywhere on Reddit with the following syntax:

    /u/username low high
    +/u/username low high

For example:

    triggerword 1000 99999
    triggerword2 -100 1000
    /u/username 0 100
    +/u/username 1 moon

*This bot was originally created for dogecoin giveaways, so "moon" is equivalent to 384400, the distance in KMs to the moon.*

## Requirements

This bot requires the following:
* Python 2.7.x
* The Python [PRAW](https://praw.readthedocs.org/) library (easy_install PRAW)
* An operating system that supports [random.SystemRandom](http://docs.python.org/2/library/random.html#random.SystemRandom) (most major operating systems are supported)

## Installation

First clone this repository. 

Copy bot.ini.dist to bot.ini and change the settings however you see fit.

For example, if I wanted to support calls like the following on the /r/radmathforthewin or /r/ilovemathohyeah subreddits:

    givemearandombetween 5 1000

You would use the following configuration file:

    [General]
    url = Bot URL, or some other unique string here
    summary = A summary of your bot by your username
    reddit_username = randnumbot
    reddit_password = bot-password
    subreddit_triggers = givemearandombetween
    subreddits = radmathforthewin,ilovemathohyeah

Note that this would also respond to the following requests across Reddit:

    /u/randnumbot 0 1000
    +/u/randnumbot 1 5

## Running the Bot

To start the bot in an OS with the Bash shell (Linux, etc...), just fire up bot-monitor.sh.

For other environments, you can launch it with

    python ./bot.py 

bot-monitor.sh keeps the bot running if it dies, so I recommend creating something similar in your chosen OS.

## Support and Bug Reports

I plan on using GitHub to manage issues, so file away.