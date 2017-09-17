import random
import pandas

def run_world(world,n_days=-1):
    day = 0
    days_reports = []
    while day < n_days:
        d = world.one_day()
        if not d:
            return days_reports
            break
        else:
            days_reports.append(d)
            day += 1
