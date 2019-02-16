Date.prototype.isWeekday = function() {
    return this.getDay() < 5;
}

function incrementDate(date) {
    const newDate = new Date(date.valueOf());
    newDate.setDate(newDate.getDate() + 1);
    return newDate;
}

function shuffle(a) {
    for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
}

function createDateRange(startDate, endDate, breakStartDate, breakEndDate) {
    const dateRange = [];
    let numWeekdays = 0;
    let numWeekends = 0;
    for (let date = startDate; date <= endDate; date = incrementDate(date)) {
        if (!(breakStartDate && breakEndDate) ||
            !(date >= breakStartDate && date <= breakEndDate)) {
            dateRange.push(date);
            if (date.isWeekday()) {
                numWeekdays++;
            } else {
                numWeekends++;
            }
        }
    }
    return {
        date_range: dateRange,
        num_weekdays: numWeekdays,
        num_weekends: numWeekends,
    };
}

function isValid(person, day, date, prev, prev_prev) {
    if (person.daysOfWeek[day]) {
        return false;
    } else if (person.dates.includes(date)) {
        return false;
    } else if (prev == person.name && prev_prev == person.name) {
        return false;
    }
    return true;
}

function createSchedule(people, startDate, endDate, breakStartDate, breakEndDate) {
    const scheduleInitInfo = createDateRange(startDate, endDate, breakStartDate, breakEndDate);
    const scheduleDateRange = scheduleInitInfo.date_range;
    const totalNumWeekdays = scheduleInitInfo.num_weekdays;
    const totalNumWeekends = scheduleInitInfo.num_weekends;

    const weekdaysPer = Math.ceil(totalNumWeekdays / people.length) + 1;
    const weekendsPer = Math.ceil(totalNumWeekends / people.length) + 1;

    let weekdaysList = [];
    let weekendsList = [];
    people.forEach((person) => {
        for (let i = 0; i < weekdaysPer; i++) {
            weekdaysList.push(person);
        }
        for (let j = 0; j < weekendsPer; j++) {
            weekendsList.push(person);
        }
    });

    let i = 0;
    while (weekdaysList.length > totalNumWeekdays) {
        const index = weekdaysList.indexOf(people[i % people.length]);
        if (index !== -1) {
            weekdaysList.splice(index, 1);
        }
        i++;
    }
    let j = 0;
    while (weekendsList.length > totalNumWeekends) {
        const index = weekendsList.indexOf(people[i % people.length]);
        if (index !== -1) {
            weekendsList.splice(index, 1);
        }
        j++;
    }


    weekdaysList = shuffle(weekdaysList);
    weekendsList = shuffle(weekendsList);

    const schedule = {}
    let prev_prev = '';
    let prev = '';
    scheduleDateRange.forEach((date) => {
        const day = date.getDay();
        let lstToUse = (date.isWeekday()) ? weekdaysList : weekendsList;
        const numLeft = lstToUse.length;
        let roll;
        let person;
        let attempts = 0;
        let found = false;
        while (attempts < people.length && !found) {
            roll = Math.floor(Math.random() * numLeft);
            person = lstToUse[roll];
            if (isValid(person, day, date, prev, prev_prev)) {
                schedule[date] = { name: person.name, is_valid: true }
                found = true;
            }
            attempts++;
        }
        if (!found) {
            roll = Math.floor(Math.random() * lstToUse.length);
            person = lstToUse[roll];
            schedule[date] = { name: person.name, is_valid: false };
        }
        lstToUse.splice(roll, 1);
        prev_prev = prev;
        prev = person.name;
    });

    return {
        schedule,
        dateRange: scheduleDateRange,
    };
}

module.exports = { createSchedule };
