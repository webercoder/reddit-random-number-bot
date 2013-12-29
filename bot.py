#!/usr/bin/env python
import time
import praw
import sys
import re
import traceback
from random import randint

keywords = ("dogerandomnumber", "/u/dogerandomnumber", "+/u/dogerandomnumber")
subreddits = ("dogemarket", "dogecoin")
already_done = []

r = praw.Reddit("Random number generator by /u/dogerandomnumber "
                "https://gist.github.com/weberwithoneb/8165498")
r.login("username", "password")

def handle_ratelimit(func, *args, **kwargs):
    while True:
        try:
            func(*args, **kwargs)
            break
        except praw.errors.RateLimitExceeded as error:
            print("Rate limit exceeded. Sleeping for %d seconds" % (error.sleep_time))
            time.sleep(error.sleep_time)

def num(val):
    try:
        return int(val)
    except ValueError:
        return 1

def reply_usage(submission):
    reply = "You may be doing something incorrectly. Please enter the following command to use this bot: \"%s x y\" (where x and y are integers)." % keywords[0]
    handle_ratelimit(submission.reply, reply)

while True:
    for subreddit_name in subreddits:
        subreddit = r.get_subreddit(subreddit_name)
        print("Getting comments for subreddit: %s" % (subreddit_name))
        for submission in subreddit.get_comments():
            print("Checking submission: %s" % (str(submission.id)))
            current_id = 0
            try:
                if submission.id not in already_done:
                    comment_text = submission.body.lower()
                    comment_text_lines = comment_text.split("\n")
                    results = []
                    for line in comment_text_lines:
                        if line.startswith(keywords):
                            current_id = submission.id
                            print("Found line, '%s'" % line)
                            try:
                                user,x,y = line.split()
                            except:
                                already_done.append(submission.id)
                                print("Invalid syntax. Skipped.")
                                reply_usage(submission)
                                continue 
                            if x is None or y is None: 
                                already_done.append(submission.id)
                                print("Invalid syntax. Skipped.")
                                reply_usage(submission)
                                continue 
                            print("Found parts: %s, %s, %s" % (user, x, y))
                            try:
                                if not x is None and x.lower() == "moon":
                                    x = 384400 # distance to the moon in kms
                                if not y is None and y.lower() == "moon":
                                    y = 384400 # distance to the moon in kms
                            except:
                                print "Error finding moon: ", sys.exc_info()[0]
                            print "x, y = %s, %s" % (str(x), str(y)) 
                            xInt = num(x)
                            yInt = num(y)
                            if xInt > yInt:
                                tmpInt = xInt
                                xInt = yInt
                                yInt = tmpInt
                            randnum = randint(xInt, yInt)
                            reply = "Random Number between %d and %d is %d." % (xInt, yInt, randnum)
                            print(reply)
                            results.append(reply)
                            already_done.append(submission.id)
                            continue
                    if len(results) > 0:
                        reply = "   \n".join(results)
                        results = []
                        print("Posting comment for %s:\n%s" % (submission.id, reply))
                        handle_ratelimit(submission.reply, reply)

            except:
                print "Unknown exception: ", sys.exc_info()[0]
                print traceback.format_exc()
                already_done.append(current_id)
                reply_usage(submission)
                continue
    time.sleep(30)

