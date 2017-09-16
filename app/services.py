import random

def run_world(world,n_days=-1):
    day = 0
    while day < n_days:
        if not world.one_day():
            break
        else:
            day += 1
