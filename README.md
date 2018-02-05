# jhu-reslife-duty-scheduler

### Installation 
To use this program you need to have Python 2.7+ installed: https://www.python.org/downloads/.
You need to clone the repo (if you know what that means you know how to do it 😀) or download the zip. 

### Usage
To use this program:
1. Create an input text file with the format
    person1 | day_of_week1, day_of_week2, ... | date1, date2, ...
    day_of_weekN is the day of the week when person1 can't do duty (ie monday, tuesday, etc)
    dateN is a specific date where person1 can't do duty (format MM/DD/YYYY) (ie 01/10/2018)
2. Save the input file as a text file (someFile.txt) in the same place that you've cloned / downloaded this repo.
3. Open your terminal and navigate to the place where you've cloned / downloaded this repo and type:
    ```
    $ python scheduler.py someFile.txt
    ```
    The program should output the total number of weekday and weekend assignments for each person and any days where a conflict still exists. 
4. If the program ran with no errors a file (schedule_someFile.txt) should have been generated with a randomized duty schedule based on the restrictions given in someFile. 

### To Do
* Create more dynamic command line flags.
* Integrate with Google Calendar API.
* Create GUI (wxPython).
* Create option for dynamic input.
