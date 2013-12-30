from datetime import datetime

# Stdout Logging
def bot_stdout_print(msg):
    curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("%s\t%s" % (curr_time, msg))

# Reddit will sometimes give ratelimit errors. This will delay posting a comment until the wait time is over.
def handle_ratelimit(func, *args, **kwargs):
    while True:
        try:
            func(*args, **kwargs)
            break
        except praw.errors.RateLimitExceeded as error:
            bot_stdout_print("Rate limit exceeded. Sleeping for %d seconds" % (error.sleep_time))
            time.sleep(error.sleep_time)
