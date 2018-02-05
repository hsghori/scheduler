import numpy as np
from datetime import date, timedelta
import sys
import random as rand
import math

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
	 name: The RA's name
	 unv_regular: The restricted days of the week
	 unv_irregular: the restricted specific dates
	'''

	def __init__(self, name='', unv_regular=set(), unv_irregular=set()):
		self.name = name 
		self.unv_regular = unv_regular
		self.unv_irregular = unv_irregular

	def __str__(self):
		return 'Name: %s\nDays Restriction: %s\nDates Restriction %s' % (self.name, str(self.unv_regular), str(self.unv_irregular))

def get_date_obj(s):
	'''
	 s is a string of the form m/d/yyyy or mm/dd/yyyy
	'''
	parts = s.split('/')
	if len(parts[2]) == 2:
		parts[2] = '20' + parts[2]
	return date(int(parts[2]), int(parts[0]), int(parts[1]))


def create_date_range(begin_str, end_str, exclude=None):
	'''
	 Creates a list of dates from begin to end excluding the dates in the exclude list.
	 begin_str and end_str are strings of the form or m/d/yyyy mm/dd/yyyy
	'''
	curr = get_date_obj(begin_str)
	end = get_date_obj(end_str)
	ret = list()
	weekdays, weekends = 0, 0
	while curr <= end:
		if exclude == None or not curr in exclude:
			ret.append(curr)
			if curr.weekday() < 5:
				weekdays += 1 
			else:
				weekends += 1
		curr = curr + dayiter
	return (ret, weekdays, weekends)

def parse_file(fn='test.txt'):
	infile = open(fn, 'r')
	ras = []
	for line in infile:
		parts = line.split('|')
		name = parts[0].strip()
		parts[1] = parts[1].replace(' ', '').strip().lower()
		regular = set([days[d] for d in parts[1].split(',')]) if parts[1] != '' else set()
		parts[2] = parts[2].replace(' ', '').strip()
		irregular = set([get_date_obj(i) for i in parts[2].split(',')]) if parts[2] != '' else set()
		ras.append(RA(name=name, unv_regular=regular, unv_irregular=irregular))
	return ras




def create_schedule(ras, start='2/16/2018', end='5/18/2018', breaks=None, name='test'):
	spring_break = create_date_range('3/17/2018', '3/24/2018')[0]
	num_ras = len(ras)
	duty_range, num_weekdays, num_weekends = create_date_range(start, end, spring_break)
	weekdays_per = int(math.ceil(num_weekdays / float(num_ras)))
	weekends_per = int(math.ceil(num_weekends / float(num_ras)))
	print num_weekdays, num_weekends, weekdays_per, weekends_per, len(ras)
	weekdays_list, weekends_list = [], []
	outfile = open('schedule_%s.txt' % name, 'w')
	tracker, schedule = dict(), dict()
	for ra in ras:
		for wk in range(weekdays_per):
			weekdays_list.append(ra)
		for we in range(weekends_per):
			weekends_list.append(ra)
		tracker[ra.name] = [weekdays_per, weekends_per]
	rand.shuffle(weekdays_list)
	rand.shuffle(weekends_list)
	count = 0
	for curr in duty_range:
		day = curr.weekday()
		if day != 4 and day != 5: # weekday
			lst, ind = weekdays_list, 0
		else:
			lst, ind = weekends_list, 1
		N = len(lst)
		attempts = 0
		found = False
		while attempts < num_ras:
			roll = rand.randint(0, N - 1)
			selected = lst[roll]
			# valid_roll = selected RA has weekdays left and day is not a conflict and date is not a conflict
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
		# print '%s : %s : %s\n' % (inverse[curr.weekday()], str(curr), schedule[curr])
	outfile.close()
	for ra in ras:
		curr = tracker[ra.name]
		print '%s : weekdays %d, weekends %d' % (ra.name, weekdays_per - curr[0], weekends_per - curr[1])

def run():
	fn = sys.argv[1]
	ras = parse_file(fn)
	create_schedule(ras, name=fn.split('.')[0])

if __name__ == '__main__':
	run()
