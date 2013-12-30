import util
import traceback
import sys
from MessageParser import MessageParser

class SubredditWatcher:

    MAX_ALREADY_DONE_LENGTH = 2000

    def __init__(self, name, praw_reddit, triggers, username):
        self.name = name
        self.praw_reddit = praw_reddit
        self.triggers = triggers
        self.username = username
        self.already_done = []
        self.msg_parser = MessageParser(triggers)

    def watch(self):
        subreddit = self.praw_reddit.get_subreddit(self.name)
        util.bot_stdout_print("Getting comments for subreddit: %s" % (self.name))
        for submission in subreddit.get_comments():
            if submission.id not in self.already_done:
                try:
                    msg = submission.body
                    successes,failures = self.msg_parser.parse(msg)
                    self.already_done.append(submission.id)
                    reply = self.get_reply(submission, successes, failures)
                    if not reply is None:
                        util.bot_stdout_print("Reply to %s: %s\n" % (submission.id, reply))
                        util.handle_ratelimit(submission.reply, reply)
                except:
                    util.bot_stdout_print("Unknown exception: %s" % sys.exc_info()[0])
                    print traceback.format_exc()
                    self.already_done.append(submission.id)
        self.cleanup_already_done()

    def get_reply(self, submission, successes, failures):

        if len(successes) > 0:
            success_msgs = []
            for result in successes:
                success_msgs.append("Random integer between %d and %d is %d." % (result["x"], result["y"], result["randnum"]))
            reply = "  \n".join(success_msgs)
            return reply

        elif len(failures) > 0:
            failure_messages = []
            for failure_msg in failures:
                failure_messages.append("* %s" % failure_msg)
            reply = "The following errors occurred:  \n  \n"
            reply += "  \n".join(failure_messages)
            reply += "  \n  \nYou may be doing something incorrectly."
            reply += " Please enter the following command to use this bot: "
            reply += "\"/u/%s x y\" (where x and y are integers)." % self.username
            return reply

    def cleanup_already_done(self):
        # Thought about just removing everything that is not in the current reddit comment list, 
        # but I'm not sure how reddit handles comment deletion. I'd hate for the bot to respond twice.
        # Instead, I'm just going to keep the list at a maximum length. This will at least keep the 
        # bot from consuming too much memory.
        if len(self.already_done) > self.MAX_ALREADY_DONE_LENGTH:
            negative_length = -1 * self.MAX_ALREADY_DONE_LENGTH
            self.already_done = self.already_done[negative_length:]
