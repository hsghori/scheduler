from datetime import date, timedelta
import random as rand
import math
try:
    import argparse
except ImportError:
    import pip
    pip.main(['install', 'argparse'])
    import argparse

days = {
        'monday': 0, 
        'tuesday': 1, 
        'wednesday': 2, 
        'thursday': 3, 
        'friday': 4, 
        'saturday': 5, 
        'sunday': 6
       }
inverse = {
        0: 'monday',
        1: 'tuesday',
        2: 'wednesday',
        3: 'thursday',
        4: 'friday',
        5: 'saturday',
        6: 'sunday'
        }

dayiter = timedelta(1)

class RA:
    '''
     Class to represent a single RA.

     Params:
     name          -> The RA's name
     unv_regular   -> The restricted days of the week
     unv_irregular -> the restricted specific dates
    '''

    def __init__(self, name='', unv_regular=set(), unv_irregular=set()):
        self.name = name 
        self.unv_regular = unv_regular
        self.unv_irregular = unv_irregular

    def __str__(self):
        return 'Name: %s\nDays Restriction: %s\nDates Restriction %s' % (self.name, str(self.unv_regular), str(self.unv_irregular))

class InvalidDateRangeException(Exception):
    '''
     Exception that represents invalid date ranges. 

     Params:
     date1 -> the start date
     date2 -> the end date
    '''

    def __init__(self, date1, date2):
        self.date1 = date1 
        self.date2 = date2

    def __str__(self):
        return 'Start date %s is later than end date %s' % (self.date1, self.date2)

class InvalidFileFormatException(Exception):
    '''
     Exception that represents invalid input file. 
    '''

    def __str__(self):
        return 'Input file format is invalid.'

def get_date_obj(s):
    '''
     Returns a date object based on an input string.
     Params:
     s -> a string of the form m/d/yyyy, mm/dd/yyyy, or mm/dd/yy
    '''
    parts = s.split('/')
    if len(parts[2]) == 2:
        parts[2] = '20' + parts[2]
    return date(int(parts[2]), int(parts[0]), int(parts[1]))


def create_date_range(begin_str, end_str, exclude=set()):
    '''
     Creates a list of dates from begin to end excluding the dates in the exclude list.

     Params:
     begin_str -> a string representing the beginning of the date range 
     end_str   -> a string representing the end of the date range
     exclude   -> a set of dates to exclude from the date range.
     
     Returns:
     ret      -> a list object containing all dates in the desired range
     weekdays -> the number of weekdays in the range
     weekends -> the number of weekends in the range
    '''
    curr = get_date_obj(begin_str)
    end = get_date_obj(end_str)
    if end < curr:
        raise InvalidDateRangeException(curr, end)
    ret = list()
    weekdays, weekends = 0, 0
    while curr <= end:
        if curr not in exclude:
            ret.append(curr)
            if curr.weekday() < 5:
                weekdays += 1 
            else:
                weekends += 1
        curr = curr + dayiter
    return (ret, weekdays, weekends)

def parse_file(infile):
    '''
     Parses a (prooperly formatted) input file and returns a list of RA objects.

     Params:
     infile -> a file object

     Returns:
     ras -> a list of RA objects based on the data in infile
    '''
    try:
        ras = []
        for line in infile:
            parts = line.split('|')
            if len(parts) <= 1:
                continue
            name = parts[0].strip()
            parts[1] = parts[1].replace(' ', '').strip().lower()
            regular = set([days[d] for d in parts[1].split(',')]) if parts[1] != '' else set()
            parts[2] = parts[2].replace(' ', '').strip()
            irregular = set([get_date_obj(i) for i in parts[2].split(',')]) if parts[2] != '' else set()
            ras.append(RA(name=name, unv_regular=regular, unv_irregular=irregular))
    except Exception:
        raise InvalidFileFormatException
    return ras

def create_schedule(ras, outfile, start='2/16/2018', end='5/18/2018', break_start='3/17/2018', break_end='3/24/2018'):
    '''
     Creates a duty schedule based on the data in ras a outputs to an outfile. 

     Params:
     ras -> a list of RA objects
     outfile -> a file object to be written to
     start -> the starting date
     end -> the ending date
     break_start -> the starting date for a major break (Thanksgiving / Spring)
     break_end -> the ending date for a major break (Thanksgiving / Spring)
    '''
    spring_break = create_date_range(break_start, break_end)[0]
    num_ras = len(ras)
    duty_range, num_weekdays, num_weekends = create_date_range(start, end, spring_break)
    weekdays_per = int(math.ceil(num_weekdays / float(num_ras)))
    weekends_per = int(math.ceil(num_weekends / float(num_ras)))
    weekdays_list, weekends_list = [], []
    tracker, schedule = dict(), dict()
    for ra in ras:
        for wk in range(weekdays_per):
            weekdays_list.append(ra)
        for we in range(weekends_per):
            weekends_list.append(ra)
        tracker[ra.name] = [weekdays_per, weekends_per]
    rand.shuffle(weekdays_list)
    rand.shuffle(weekends_list)
    for curr in duty_range:
        day = curr.weekday()
        if day != 4 and day != 5: # weekday
            lst, ind = weekdays_list, 0
        else: #weekend
            lst, ind = weekends_list, 1
        N = len(lst)
        attempts = 0
        found = False
        while attempts < num_ras:
            roll = rand.randint(0, N - 1)
            selected = lst[roll]
            valid = day not in selected.unv_regular and curr not in selected.unv_irregular and schedule.get(curr - dayiter, 'None') != selected.name
            if valid:
                schedule[curr] = selected.name
                found = True
                break
            attempts += 1
        if not found:
            print '%s - Couldn\'t resolve' % str(curr)
            roll = rand.randint(0, N - 1)
            selected = lst[roll]
            schedule[curr] = selected.name
        nm = lst.pop(roll).name 
        tracker[nm][ind] -= 1
    for curr in duty_range:
        outfile.write('%s : %s : %s\n' % (inverse[curr.weekday()], str(curr), schedule[curr]))
    outfile.close()
    print 'Summary'
    for ra in ras:
        curr = tracker[ra.name]
        print '%s : weekdays %d, weekends %d' % (ra.name, weekdays_per - curr[0], weekends_per - curr[1])

def run_cl(infile, outfile, start_date, end_date):
    ras = parse_file(infile)
    create_schedule(ras, outfile, start=start_date, end=end_date)
    print('Finished schedule has been output to %s' % outfile.name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ResLife duty scheduler',
                                     prog='scheduler.py')
    parser.add_argument('-i', '--infile', type=argparse.FileType('r'), required=True,
                        help='Enter filename of preference file. Example: mccoy.txt')
    parser.add_argument('-o', '--outfile', nargs='?', type=argparse.FileType('w'),
                        default='schedule_out.txt', help='Enter name of \
                        preferred output file. Default is schedule_out.txt')
    parser.add_argument('-s', '--start-date', default='2/16/2018', 
                        help='Enter starting date in MM/DD/YYYY format.')
    parser.add_argument('-e', '--end-date', default='5/17/2018', 
                        help='Enter ending date in MM/DD/YYYY format.')
    parser.add_argument('-bs', '--break-start-date', default='3/17/2018', 
                        help='Enter the starting date of a major break \
                        (Thanksgiving / Easter) in MM/DD/YYYY format.')
    parser.add_argument('-be', '--break-end-date', default='3/24/2018', 
                        help='Enter the ending date of a major break \
                        (Thanksgiving / Easter) in MM/DD/YYYY format.')
    args = parser.parse_args()
    run_cl(args.infile, args.outfile, args.start_date, args.end_date)
