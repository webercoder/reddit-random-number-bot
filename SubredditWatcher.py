import number
import reddit
import util
import traceback
import sys

class SubredditWatcher:

    MAX_ALREADY_DONE_LENGTH = 2000

    def __init__(self, name, praw_reddit, triggers):
        self.name = name
        self.praw_reddit = praw_reddit
        self.triggers = triggers
        self.already_done = []

    def watch(self):
        subreddit = self.praw_reddit.get_subreddit(self.name)
        util.bot_stdout_print("Getting comments for subreddit: %s" % (subreddit_name))
        for submission in subreddit.get_comments():
            current_id = 0
            try:
                if submission.id not in self.already_done:
                    comment_text = submission.body.lower()
                    comment_text_lines = comment_text.split("\n")
                    results = []
                    for line in comment_text_lines:
                        if line.startswith(self.triggers):
                            current_id = submission.id
                            util.bot_stdout_print("Found line, '%s'" % line)
                            try:
                                user,x,y = line.split()
                            except:
                                self.already_done.append(submission.id)
                                util.bot_stdout_print("Invalid syntax. Skipped.")
                                reply_usage(submission)
                                continue 
                            if x is None or y is None: 
                                self.already_done.append(submission.id)
                                util.bot_stdout_print("Invalid syntax. Skipped.")
                                reply_usage(submission)
                                continue 
                            util.bot_stdout_print("Found parts: %s, %s, %s" % (user, x, y))
                            try:
                                if not x is None and x.lower() == "moon":
                                    x = 384400 # distance to the moon in kms
                                if not y is None and y.lower() == "moon":
                                    y = 384400 # distance to the moon in kms
                            except:
                                util.bot_stdout_print("Error finding moon: %s" % sys.exc_info()[0])
                            util.bot_stdout_print("x, y = %s, %s" % (str(x), str(y)))
                            xInt = number.num(x)
                            yInt = number.num(y)
                            if xInt > yInt:
                                tmpInt = xInt
                                xInt = yInt
                                yInt = tmpInt
                            randnum = number.so_random(xInt, yInt)
                            reply = "Random Number between %d and %d is %d." % (xInt, yInt, randnum)
                            util.bot_stdout_print(reply)
                            results.append(reply)
                            self.already_done.append(submission.id)
                            continue
                    if len(results) > 0:
                        reply = "   \n".join(results)
                        results = []
                        util.bot_stdout_print("Posting comment for %s:\n%s" % (submission.id, reply))
                        reddit.handle_ratelimit(submission.reply, reply)
            except:
                util.bot_stdout_print("Unknown exception: %s" % sys.exc_info()[0])
                print traceback.format_exc()
                self.already_done.append(current_id)
                reply_usage(submission)
                continue
        cleanup_already_done()

    def cleanup_already_done(self):
        # Thought about just removing everything that is not in the current reddit comment list, 
        # but I'm not sure how reddit handles comment deletion. I'd hate for the bot to respond twice.
        # Instead, I'm just going to keep the list at a maximum length. This will at least keep the 
        # bot from consuming too much memory.
        if len(self.already_done) > MAX_ALREADY_DONE_LENGTH:
            negative_length = -1 * MAX_ALREADY_DONE_LENGTH
            self.already_done = self.already_done[negative_length:]

    # Post a reddit comment about proper usage when someone uses this bot incorrectly.
    def reply_usage(submission):
        reply = "You may be doing something incorrectly. Please enter the following command to use this bot: \"%s x y\" (where x and y are integers)." % self.triggers[0]
        reddit.handle_ratelimit(submission.reply, reply)
