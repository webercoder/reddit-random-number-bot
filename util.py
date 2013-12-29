from datetime import datetime

# Stdout Logging
def bot_stdout_print(msg):
    curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("%s\t%s" % (curr_time, msg))