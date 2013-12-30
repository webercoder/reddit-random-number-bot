import util
import traceback
import sys
import time
from MessageParser import MessageParser

class MentionsWatcher:

    MAX_ALREADY_DONE_LENGTH = 2000
    DELAY = 30

    def __init__(self, praw_reddit, username):
        self.praw_reddit = praw_reddit
        self.username = username
        self.already_done = []
        self.last_run = None
        self.msg_parser = MessageParser(username=username)

    def watch(self):
        now = int(time.time())
        if self.last_run is None or now - self.last_run > self.DELAY:
            util.bot_stdout_print("Getting mentions for user: %s" % (self.username))
            mentions = self.praw_reddit.get_mentions()
            self.last_run = int(time.time())
            try:
                for mention in mentions:
                    if mention.new == True and mention.id not in self.already_done:
                        msg = mention.body
                        successes,failures = self.msg_parser.parse(msg)
                        reply = self.get_reply(successes, failures)
                        self.already_done.append(mention.id)
                        mention.mark_as_read()
                        if not reply is None:
                            util.bot_stdout_print("Reply to %s: %s\n" % (mention.id, reply))
                            util.handle_ratelimit(mention.reply, reply)
            except:
                util.bot_stdout_print("Unknown exception: %s" % sys.exc_info()[0])
                print traceback.format_exc()
                self.already_done.append(mention.id)
            self.cleanup_already_done()

    def get_reply(self, successes, failures):
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
        if len(self.already_done) > self.MAX_ALREADY_DONE_LENGTH:
            negative_length = -1 * self.MAX_ALREADY_DONE_LENGTH
            self.already_done = self.already_done[negative_length:]

