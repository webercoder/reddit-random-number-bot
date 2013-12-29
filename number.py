from random import SystemRandom

# Get an integer from a specified upper or lower value.
def num(val):
    try:
        return int(val)
    except ValueError:
        return 1

# Get a random number from the system. It must be within the specified bounds.
def so_random(x, y):
    return SystemRandom().randint(x, y)
