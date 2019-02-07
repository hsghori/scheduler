let _ = require('lodash');

function incrementDate(date) {
    const newDate = new Date(date.valueOf());
    newDate.setDate(newDate.getDate() + 1);
    return newDate
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
        if (!(date >= breakStartDate && date <= breakEndDate)) {
            dateRange.push(date);
            if (date.getDay() > 0 && date.getDay() < 5) {
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

function createSchedule(people, startDate, endDate, breakStartDate, breakEndDate) {
    if (!(breakStartDate && breakEndDate)) {
        return { schedule: {}, scheduleDateRange: [] };
    }

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

    weekdaysList = shuffle(weekdaysList);
    weekendsList = shuffle(weekendsList);

    const schedule = {}
    let prev = '';
    scheduleDateRange.forEach((date) => {
        const day = date.getDay();
        let lstToUse = (day != 4 && day != 5) ? weekdaysList : weekendsList;
        const numLeft = lstToUse.length;

        let attempts = 0;
        let roll;
        let person;
        let found = false;
        while (attempts < people.length && !found) {
            roll = Math.floor(Math.random() * numLeft);
            person = lstToUse[roll];
            const isValid = !(person.daysOfWeek[day] ||
                              person.dates.includes(date) ||
                              prev === person.name);
            if (isValid) {
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
        prev = person.name;
    });

    return {
        schedule,
        schedule_date_range: scheduleDateRange,
    };
}

module.exports = { createSchedule };
