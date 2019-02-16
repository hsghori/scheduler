from datetime import date
import sys
import scheduler
import argparse


def get_summary(infile):
    """
    Prints a summary of the schedule. The summary shows the number of weekdays and weekends assigned
    to each person.

    :param infile: The input schedule file
    :type infile: file
    """
    sched = scheduler.parse_sched_file(infile)
    tracker = dict()
    for curr in sched:
        parts = curr.split('-')
        d = date(int(parts[0]), int(parts[1]), int(parts[2]))
        name = sched[curr].strip()
        if name not in tracker:
            tracker[name] = [0, 0]
        if d.weekday() == 4 or d.weekday() == 5:
            tracker[name][1] += 1
        else:
            tracker[name][0] += 1
    for name in tracker:
        print '%s weekdays=%d, weekends=%d' % (name, tracker[name][0], tracker[name][1])


def check_reqs(reqs_file, sched_file):
    """
    Displays the conflicts in a specific schedule given a requirements file.

    :param reqs_file: a file with the schedule constraints
    :type reqs_file: file
    :param sched_file: a file with the schedule
    :type sched_file: file
    """
    ras = scheduler.parse_file(reqs_file)
    ras_dict = dict()
    for ra in ras:
        ras_dict[ra.name] = ra
    sched = scheduler.parse_sched_file(sched_file)
    count = 0
    for curr in sched:
        parts = curr.split('-')
        curr_date = date(int(parts[0]), int(parts[1]), int(parts[2]))
        ra = ras_dict[sched[curr]]
        if curr_date in ra.unvirregular or curr_date.weekday() in ra.unv_regular:
            print 'Conflict: %s - %s' % (curr, sched[curr])
            count += 1
    print '%d total conflicts' % (count)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ResLife duty scheduler',
                                     prog='analyze.py')
    parser.add_argument('-cr', '--check-reqs', action='store_true')
    parser.add_argument('-gs', '--get-summary', action='store_true')
    parser.add_argument('-pf', '--prefs-file', type=argparse.FileType('r'), default=None,
                        help='Enter filename of preferences file. Example: mccoy.txt')
    parser.add_argument('-sf', '--schedule-file', type=argparse.FileType('r'), default=None,
                        help='Enter filename of schedule file.')

    flags = parser.parse_args()
    if flags.check_reqs:
        if flags.prefs_file is None:
            print 'Invalid arguments: need preferences file'
            sys.exit()
        if flags.schedule_file is None:
            print 'Invalid arguments: need schedule file'
            sys.exit()
        check_reqs(flags.prefs_file, flags.schedule_file)
    if flags.get_summary:
        if flags.schedule_file is None:
            print 'Invalid arguments: need schedule file'
            sys.exit()
        get_summary(flags.schedule_file)
