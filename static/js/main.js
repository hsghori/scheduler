let $ = require('jquery');
let { pill, stop } = require('styledot/loading');
let { createForm, createScheduleRow, createAnalysisRow, DAYS } = require('./constants');
let { createSchedule } = require('./schedule');

const ADD_PERSON_BUTTON = '.js-add-person-button';
const FORM_CONTAINER = '.form-container';
const DATES_TEXT = '.js-dates-text-box';
const GENERAL_FORM = '.general-form';
const INDIVIDUAL_FORM = '.individual-form';
const CLOSE_FORM = '.js-close-form';
const COMMIT_DATE = '.js-commit-date';
const SPECIFIC_DATE_ENTRY = '.js-specific-date';
const CLEAR_DATES = '.js-clear-dates';
const SUBMIT_BUTTON = '.js-submit-button';

const SET_SCHEDULE_FORM = '.module-scheduler-form';
const SCHEDULE_MODULE = '.module-scheduler-schedule';


function getPerson(form) {
    return new Object({
        name: form.find('#name').text(),
        dates: form.find(DATES_TEXT).text().split(' ').filter(
            dateText => dateText !== ''
        ).map(
            dateText => new Date(dateText)
        ),
        daysOfWeek: DAYS.map(
            day => form.find(`#checkbox_${day}_${name}`).prop('checked')
        ),
    });
}

function commitDate(e) {
    const $this = e.target
    const date = $($this).siblings(SPECIFIC_DATE_ENTRY).val();
    if (date) {
        const currDateTextBox = $($this).parent().siblings(DATES_TEXT);
        const datesText = currDateTextBox.text();
        const newDatesText = `${datesText}${date} `;
        currDateTextBox.text(newDatesText);
    }
}

function clearDates(e) {
    const $this = e.target;
    $($this).siblings(DATES_TEXT).text('');
    $($this).siblings('.side-by-side').children(SPECIFIC_DATE_ENTRY).val('');
}

function removePerson(e) {
    $(e.target).parents(INDIVIDUAL_FORM).remove();
}

function addNewPerson() {
    const name = prompt('Enter the name');
    if (!name) {
        return;
    }

    const newForm = $($.parseHTML(createForm(name)));
    newForm.find('#name').text(name);
    newForm.find(CLOSE_FORM).on('click', removePerson);
    newForm.find(COMMIT_DATE).on('click', commitDate);
    newForm.find(CLEAR_DATES).on('click', clearDates);
    $(SUBMIT_BUTTON).removeClass('hide');
    $(FORM_CONTAINER).append(newForm);
}

function analyzeSchedule() {
    $('.analysis-table .analysis-table-body').empty();

    const aggregationObj = {};
    $(SCHEDULE_MODULE).find('.schedule-row').each((index, e) => {
        $elem = $(e);
        const name = $elem.find('#name-value').val();
        const day = new Date($elem.find('.date-cell').text()).getDay();

        if (!aggregationObj[name]) {
            aggregationObj[name] = { numWeekdays: 0, numWeekends: 0 };
        }
        if (day !== 4 && day !== 5) {
            aggregationObj[name].numWeekdays++;
        } else {
            aggregationObj[name].numWeekends++;
        }
    });
    Object.keys(aggregationObj).forEach((name) => {
        const newRow = createAnalysisRow(name, aggregationObj[name].numWeekdays, aggregationObj[name].numWeekends);
        $('.analysis-table .analysis-table-body').append(newRow);
    });
    $('.analysis-card').removeClass('hide');
}

function getFormatedString(date) {
    var yyyy = date.getFullYear().toString();
    var mm = (date.getMonth()+1).toString();
    var dd  = date.getDate().toString();

    var mmChars = mm.split('');
    var ddChars = dd.split('');

    return yyyy + '-' + (mmChars[1]?mm:"0"+mmChars[0]) + '-' + (ddChars[1]?dd:"0"+ddChars[0]);
  }

function download(filename, text) {
    let element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

function getScheduleFile() {
    let text = ''
    $(SCHEDULE_MODULE).find('.schedule-row').each((index, e) => {
        $elem = $(e);
        const name = $elem.find('#name-value').val();
        const date = new Date($elem.find('.date-cell').text());
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
        text += `${days[date.getDay()]} : ${name} : ${getFormatedString(date)}\n`
    });
    return text;
}

function populateSchedule({ schedule, dateRange }) {
    dateRange.forEach((date) => {
        const newRow = createScheduleRow(schedule[date].name, date.toLocaleDateString("en-US"), schedule[date].is_valid)
        $('.schedule-table .schedule-table-body').append(newRow);
    });
    $(SCHEDULE_MODULE).removeClass('hide');
    $('.js-analyze-button').on('click', analyzeSchedule);
    $('.js-rerun-button').on('click', () => {
        $(SCHEDULE_MODULE).find('.schedule-table-body').empty();
        $(SCHEDULE_MODULE).addClass('hide');
        $(SET_SCHEDULE_FORM).removeClass('hide');
    });
    $('.js-start-new-button').on('click', () => {
        $(SCHEDULE_MODULE).find('.schedule-table-body').empty();
        $(SCHEDULE_MODULE).addClass('hide');
        $(SET_SCHEDULE_FORM).find(FORM_CONTAINER).empty();
        $(SET_SCHEDULE_FORM).removeClass('hide');
        $(SUBMIT_BUTTON).addClass('hide');
    });
    $('.js-download-button').on('click', () => {
        const text = getScheduleFile();
        const scheduleName = $('#schedule-name').val().toLowerCase();
        download(`${scheduleName}-schedule.txt`, text);
    });
}

function getDateObject(dateString) {
    // date is of the form YYYY-MM-DD but JS date indexes month at 0.
    const splitString = dateString.split('-');
    return new Date(splitString[0], splitString[1] - 1, splitString[2]);
}

function commit() {
    const peopleList = $(FORM_CONTAINER).children(INDIVIDUAL_FORM).toArray().map(
        form => getPerson($(form))
    );

    const generalForm = $(GENERAL_FORM);
    const scheduleName = generalForm.find('#schedule-name').val();
    const startDate = generalForm.find('#start-date').val();
    const endDate = generalForm.find('#end-date').val();
    const breakStartDate = generalForm.find('#break-start-date').val();
    const breakEndDate = generalForm.find('#break-end-date').val();
    if (!(startDate && endDate)) {
        console.log('fill in start and end date', startDate, endDate);
        return;
    } else if ((!breakStartDate && breakEndDate) || (breakStartDate && !breakEndDate)) {
        console.log('both breakStartDate and breakEndDate must be defined', breakStartDate, breakEndDate);
        return;
    }
    $(SET_SCHEDULE_FORM).addClass('hide')
    pill($('body'), 'Generating schedule');
    stop($('body'), () => {
        scheduleObj = createSchedule(
            peopleList,
            getDateObject(startDate),
            getDateObject(endDate),
            breakStartDate ? getDateObject(breakStartDate) : null,
            breakEndDate ? getDateObject(breakEndDate) : null
        );
        populateSchedule(scheduleObj);
    });
}

$(document).ready(function() {
    $(ADD_PERSON_BUTTON).on('click', addNewPerson);
    $(SUBMIT_BUTTON).on('click', commit);
});
