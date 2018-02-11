# jhu-reslife-duty-scheduler
This program is designed to facilitate duty scheduling for JHU Reslife. If you want to use it for some other purpose feel free. Feel free to use and modify this program as you see fit. 
This readme is written for people with little experience with the terminal. 
 
### Installation 
To use this program you need to have Python 2.7+ installed: https://www.python.org/downloads/.
You also need to clone or download this repo. 

### Usage
To use this program:
1. Create an input text file with the format
    person1 | day_of_week1, day_of_week2, ... | date1, date2, ...
    day_of_weekN is the day of the week when person1 can't do duty (ie monday, tuesday, etc)
    dateN is a specific date where person1 can't do duty (format MM/DD/YYYY) (ie 01/10/2018)
    
    Example:
    ```
    John | Monday | 02/14/2018, 03/01/2018, 05/01/2018
    Jill | Tuesday, Wednesday | 04/10/2018, 05/13/2018
    ```
2. Save the input file as a text file (someFile.txt) in the same place that you've cloned / downloaded this repo.
3. Open your terminal and navigate to the place where you've cloned / downloaded this repo and type:
	```
    $ python scheduler.py --infile someFile.txt
	```
    The program should output the total number of weekday and weekend assignments for each person and any days where a conflict couldn't be easily resolved.  
	You can also specify the name of the output file (by default is schedule\_out.txt) via:
	```Bash
	$ python scheduler.py --infile someFile.txt --outfile someOutput.txt
	```
	__If you're using this tool past Spring 2018 you can enter new start and end dates both for the semester and for major breaks (Thanksgiving / Spring)__

	For example, the command to generate a schedule for Fall 2018 may look like:
	```Bash
	$ python scheduler.py --infile someFile.txt --outfile someOutput.txt --start-date 8/25/2018 --end-date 12/21/2018 --break-start-date 11/17/2018 --break-end-date 11/25/2018
	```
	If you need help with the commands you can type:
	```Bash
	$ python scheduler.py --help
	```
	__Note__: Each of the commands above has a less verbose version. In order they are:
	```Bash
	$ python scheduler.py -i someFile.txt
	$ python scheduler.py -i someFile.txt -o someOutput.txt
	$ python scheduler.py -i someFile.txt -o someOutput.txt -s 8/25/2018 -e 12/21/2018 -bs 11/17/2018 -be 11/25/2018
	$ python scheduler.py -h
	```
4. If the program ran with no errors a file (schedule\_out.txt) should have been generated with a randomized duty schedule based on the restrictions given in someFile. 

### Google Calendar Support 
Google calendar support is basically ready - you just need to download your own API key. (Eventually I'll try to package this so you don't have to do that, but as of now this is the best I can do.). 
Follow the steps here: https://developers.google.com/google-apps/calendar/quickstart/python to get your own Google Calendar API key. Make sure you move the client.json file to the same folder as scheduler.py. 
Once you've generated a schedule (see above) you can commit it to google calendar using:
```Bash
	$ python scheduler.py --commit --infile schedule_file.txt 
```
Or
```Bash
	$ python scheduler.py -c -i schedule_file.txt
```
The "commit" (-c) flag turns on "commit mode". There are a few other flags you can use in commit mode. Run:
```Bash 
	$ python scheduler.py -h 
```
for more detailed information. 

### Issues or Updates
If you spot some kind of bug you can approach me directly or open an issue on github. 

If you'd like to make a contribution to this repo please submit a pull request. 

### To Do
* Integrate with Google Calendar API.
* Create GUI (wxPython).
* Create option for dynamic input.
