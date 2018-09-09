import datetime
from datetime import date, timedelta
import random as rand
import math
import os
import sys
try:
    import httplib2
    from apiclient import discovery
    from oauth2client import client
    from oauth2client import tools
    from oauth2client.file import Storage
    import argparse
    from tqdm import tqdm
except ImportError:
    import pip
    pip.main(['install', 'argparse'])
    pip.main(['install', 'httplib2'])
    pip.main(['install', 'google-api-python-client'])
    pip.main(['install', 'tqdm'])
    import argparse
    import httplib2
    from apiclient import discovery
    from oauth2client import client
    from oauth2client import tools
    from oauth2client.file import Storage

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

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
         name -> The RA's name
         unv_regular -> The restricted days of the week
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
     Params:
        fn -> the filename
    '''

    def __init__(self, fn):
        self.fn = fn

    def __str__(self):
        return '%s - file format is invalid.' % (self.fn)


def get_date_obj(s):
    '''
     Returns a date object based on an input string.
     Params:
        s -> a string of the form m/d/yyyy, mm/dd/yyyy, or mm/dd/yy
    '''
    parts = s.split('/')
    if len(parts[2]) == 2:
        parts[2] = '20' + parts[2]
    print int(parts[2]), int(parts[0]), int(parts[1])
    return date(int(parts[2]), int(parts[0]), int(parts[1]))


def create_gcal_even(name, date, tag=''):
    '''
     Returns a dict event based on the given data. 
     Params:
        name -> the name of hte event 
        date -> a string representation of the date 
        tag -> an optional tag to prepend to the event title. 
     Returns:
        a dict event based on the Google Calendar API
    '''
    tag = tag + ': ' if tag != '' and tag != None else ''
    event = {
        'summary': tag + name,
        'start': {
            'date': date
        },
        'end': {
            'date': date
        }
    }
    return event


def create_date_range(begin_str, end_str, exclude=set()):
    '''
     Creates a list of dates from begin to end excluding the dates in the exclude list.
     Params:
         begin_str -> a string representing the beginning of the date range 
         end_str -> a string representing the end of the date range
         exclude -> a set of dates to exclude from the date range.
     Returns:
         ret -> a list object containing all dates in the desired range
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
    ras = []
    for line in infile:
        try:
            parts = line.split('|')
            if len(parts) <= 1:
                continue
            name = parts[0].strip()
            parts[1] = parts[1].replace(' ', '').strip().lower()
            regular = set([days[d] for d in parts[1].split(',')]
                          ) if parts[1] != '' else set()
            parts[2] = parts[2].replace(' ', '').strip()
            irregular = set([get_date_obj(i) for i in parts[2].split(',')]) if parts[
                2] != '' else set()
            ras.append(RA(name=name, unv_regular=regular,
                          unv_irregular=irregular))
<<<<<<< HEAD
        except Exception as e:
            print e
            raise InvalidFileFormatException()
=======
    except Exception:
        raise InvalidFileFormatException(infile.name)
>>>>>>> 66cef1a8a835b1f99731bcdcb76b92292ffb5c66
    return ras


def create_schedule(ras, outfile, start, end, break_start=None, break_end=None):
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
    num_ras = len(ras)
    break_, _, _ = create_date_range(
        break_start, break_end) if break_start != None and break_end != None else set()
    duty_range, num_weekdays, num_weekends = create_date_range(
        start, end, break_)
    weekdays_per = int(math.ceil(num_weekdays / float(num_ras)))
    weekends_per = int(math.ceil(num_weekends / float(num_ras)))
    weekdays_list, weekends_list = [], []
    tracker, schedule = dict(), dict()
    for ra in ras:
        for wk in range(weekdays_per + 1):
            weekdays_list.append(ra)
        for we in range(weekends_per + 1):
            weekends_list.append(ra)
        tracker[ra.name] = [weekdays_per, weekends_per]
    rand.shuffle(ras)
    count = 0
    '''
    while len(weekdays_list) > num_weekdays:
        weekdays_list.remove(ras[count % len(ras)])
        count += 1
    '''
    rand.shuffle(ras)

    rand.shuffle(weekdays_list)
    rand.shuffle(weekends_list)

    print len(weekdays_list), len(weekends_list)
    print num_weekdays, num_weekends

    for curr in duty_range:
        day = curr.weekday()
        # print curr
        if day != 4 and day != 5:  # weekday
            lst, ind = weekdays_list, 0
        else:  # weekend
            lst, ind = weekends_list, 1
        # print curr, day
         # print lst
        N = len(lst)
        attempts = 0
        found = False
        while attempts < num_ras:
            roll = rand.randint(0, N - 1)
            selected = lst[roll]
            valid = day not in selected.unv_regular and curr not in selected.unv_irregular and schedule.get(
                curr - dayiter, 'None') != selected.name
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
        outfile.write('%s : %s : %s\n' %
                      (inverse[curr.weekday()], str(curr), schedule[curr]))
    outfile.close()
    print 'Summary'
    for ra in ras:
        curr = tracker[ra.name]
        print '%s : weekdays %d, weekends %d' % (ra.name, weekdays_per - curr[0], weekends_per - curr[1])


def get_credentials():
    '''
     Gets valid user credentials from storage.
     If nothing has been stored, or if the stored credentials are invalid,
     the OAuth2 flow is completed to obtain the new credentials.
     Returns:
        Credentials, the obtained credential.
    '''
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'duty-scheduler.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def parse_sched_file(sched_file):
    '''
     Parses a schedule file of the format created when autogenerating a schedule.
     Params:
        sched_file -> a file handle for the file containing the schedule
     Returns:
        a dictionary representation of the schedule
    '''
    sched = dict()
    lines = sched_file.readlines()
    i = 1
    try:
        for line in lines:
            parts = line.split(' : ')  # day of week : date : name
            sched[parts[1]] = parts[2]
            i += 1
        return sched
    except Exception as e:
        raise InvalidFileFormatException(sched_file.name)
        print 'File format error on line %d' % (i)


def commit_sched(sched, tag='', calID=''):
    '''
     Uses the Google Calendar API to commit a schedule dict to a Google Calendar.
     Params:
        sched -> a dictionary that maps string dates to names
        tag -> an optional tag 
        calID -> the Google Calendar ID
    '''
    calID = calID if calID != '' else raw_input('Enter the calendar id for your google calendar.\n\
                                                  On google calendar go your calendar\'s settings \
                                                  and find the Calendar ID entry\n-> ')
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    for curr in tqdm(sched):
        try:
            event = create_gcal_even(sched[curr].strip(), curr, tag)
            service.events().insert(calendarId=calID, body=event).execute()
        except Exception as e:
            print 'Failed to update %s' % curr
            print e
            while True:
                cont = raw_input('Continue? (Y/N) -> ')
                if cont.lower() == 'y':
                    break
                elif cont.lower() == 'n':
                    sys.exit()


def run_commit(infile, staff, calID):
    choose = raw_input('You\'ve entered commit mode which allows you to upload\
             a generated schedule to Google Calendar. For this to work \
             properly you need to have a Google Calender API key ( \
             client_secret.json), a Google account, and an editable Google \
             Calendar with a Calendar ID.\nIf you don\'t meet one or more of \
             those criteria, enter N to \
               quit. Otherwise enter Y to continue.\n-> ')
    choose = choose.lower()
    while choose != 'y' and choose != 'n':
        choose = raw_input('Enter Y to continue or N to quit -> ').lower()
    if choose == 'n':
        sys.exit()
    # assume that infile is the schedule file
    sched = parse_sched_file(infile)
    print(sched)
    while True:
        choice = raw_input('Are you sure you want to commit this schedule?\
                          (Y/N) -> ')
        if choice.lower() == 'y':
            commit_sched(sched, tag=staff, calID=calID)
            return
        elif choice.lower() == 'n':
            return


def run_create(infile, outfile, start_date, end_date, break_start, break_end):
    '''
     Creates a schedule based on data in infile and outptus to outfile. 
     Params:
        infile -> an input file handle 
        outfile -> an output file handle 
        start_date -> the start date for the schedule 
        end_date -> the end date for the schedule
    '''
    ras = parse_file(infile)
    create_schedule(ras, outfile, start=start_date, end=end_date,
                    break_start=break_start, break_end=break_end)
    print 'Finished schedule has been output to %s.\n \
           Please look over schedule before commiting to Google Calendar.\n \
           Run \'$ python scheduler.py -i %s -c\' to commit to Google Calendar.' % (outfile.name, outfile.name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ResLife duty scheduler',
                                     parents=[tools.argparser],
                                     prog='scheduler.py')
    parser.add_argument('-i', '--infile', type=argparse.FileType('r'),
                        required=True,
                        help='Enter filename of preference file. Example: \
                        mccoy.txt')
    parser.add_argument('-o', '--outfile', nargs='?',
                        type=argparse.FileType('w'),
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
    parser.add_argument('-c', '--commit', action='store_true')
    parser.add_argument('-st', '--staff', default='',
                        help='The staff (for organizational purposes) - commit\
                         mode only.')
    parser.add_argument('-cal', '--calendar-id', default='',
                        help='The google calendar id - commit mode only')
    flags = parser.parse_args()
    if flags.commit:  # commit mode
        run_commit(flags.infile, flags.staff, flags.calendar_id)
    else:  # create mode
        run_create(flags.infile, flags.outfile, flags.start_date,
                   flags.end_date, flags.break_start_date,
                   flags.break_end_date)
