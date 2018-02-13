from datetime import date
import sys

def parse_sched_file(fn):
    '''
     Parses a schedule file of the format created when autogenerating a schedule.
     Params:
        sched_file -> a file handle for the file containing the schedule
     Returns:
        a dictionary representation of the schedule
    '''
    sched_file = open(fn, 'r')
    sched = dict()
    lines = sched_file.readlines()
    for line in lines:
        parts = line.split(' : ') # day of week : date : name
        sched[parts[1]] = parts[2]
    return sched

sched = parse_sched_file(sys.argv[1])
tracker = dict()
for curr in sched:
    parts = curr.split('-')
    d = date(int(parts[0]), int(parts[1]), int(parts[2]))
    name = sched[curr].strip()
    if name not in tracker:
        tracker[name] = [0, 0]
    if d.weekday() == 4 or d.weekday() == 5:
        tracker[name][1]+=1
    else:
        tracker[name][0]+=1
for name in tracker:
    print '%s weekdays=%d, weekends=%d' % (name, tracker[name][0], tracker[name][1])
