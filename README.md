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
2. Save the input file as a text file (someFile.txt)
3. Open your terminal and navigate to the place where you've cloned / downloaded this repo and type:
    ```
    $ python scheduler.py someFile.txt
    ```
