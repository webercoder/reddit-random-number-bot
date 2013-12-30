import number
import util
from random import SystemRandom

class MessageParser:
    
    def __init__(self, triggers):
        self.triggers = triggers
        self.username = username

    def parse(self, msg):
        successes = []
        failures = []
        msg = msg.lower()
        msg_lines = msg.split("\n")
        for line in msg_lines:
            try:
                successes.append(self.parse_line(line))
            except e:
                failures.append(str(e))
        return {'successes':successes, 'failures':failures}

    def parse_line(self, line):
        username_mention = "/u/%s" % self.username;
        if line.startswith(self.triggers) or line.startswith(username_mention):
            x,y = extract_numbers(line)
            randnum = self.so_random(x, y)
            return {'x':x, 'y':y, 'random':randnum}

    def extract_numbers(self, line):
        try:
            user,x,y = line.split()
        except:
            raise Exception("Unable to split the line into three parts for user, x, and y.")

        if x is None or y is None: 
            raise Exception("A lower and upper value are currently required.")

        try:
            if not x is None and x.lower() == "moon":
                x = 384400 # distance to the moon in kms
            if not y is None and y.lower() == "moon":
                y = 384400 # distance to the moon in kms
        except:
            raise Exception("Unable to determine if x or y == 'moon'.")

        xInt = self.num(x)
        yInt = self.num(y)

        if xInt > yInt:
            tmpInt = xInt
            xInt = yInt
            yInt = tmpInt

        return x,y


    # Get an integer from a specified upper or lower value.
    def num(val):
        try:
            return int(val)
        except:
            return 1

    # Get a random number from the system. It must be within the specified bounds.
    def so_random(x, y):
        return SystemRandom().randint(x, y)
