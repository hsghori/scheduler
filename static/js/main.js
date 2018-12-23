let $ = require('jquery');
let { pill, stop } = require('styledot/loading');
let { createForm, DAYS } = require('./constants');
let { createSchedule } = require('./schedule');

const ADD_PERSON_BUTTON = '.js-add-person-button';
const NEW_PERSON_FORM = '.form-template';
const FORM_CONTAINER = '.form-container';
const DATES_TEXT = '.js-dates-text-box';
const GENERAL_FORM = '.general-form';
const INDIVIDUAL_FORM = '.individual-form';
const CLOSE_FORM = '.js-close-form';
const COMMIT_DATE = '.js-commit-date';
const SPECIFIC_DATE_ENTRY = '.js-specific-date';
const CLEAR_DATES = '.js-clear-dates';
const SUBMIT_BUTTON = '.js-submit-button';

const SCHEDULE_MODULE = '.module-scheduler-schedule';
const TEMPLATE_SCHEDULE_ROW = '.schedule-template-row';


function getPerson(form) {
    return new Object({
        name: form.find('#name').val(),
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

    $(FORM_CONTAINER).append(newForm);
}

function populateSchedule() {
    scheduleObj = createSchedule(
        peopleList, 
        new Date(startDate), 
        new Date(endDate), 
        breakStartDate ? new Date(breakStartDate) : null, 
        breakEndDate ? new Date(breakEndDate) : null
    );
    const schedule = scheduleObj.schedule;
    const dateRange = scheduleObj.schedule_date_range;
    dateRange.forEach((date) => {
        const newRow = $(TEMPLATE_SCHEDULE_ROW).clone();
        newRow.removeClass('hide');
        newRow.removeClass('schedule-template-row');
        newRow.addClass('schedule-row');
        newRow.find('.date-cell').text(date.toLocaleDateString("en-US"));
        newRow.find('.name-cell .name-value').text(schedule[date].name);
        newRow.find('.is-valid-cell .is-valid-value').text(schedule[date].is_valid);
    });
    $(SCHEDULE_MODULE).removeClass('hide');
}

function commit() {
    let schedule;

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
        return;
    } else if ((!breakStartDate && breakEndDate) || (breakStartDate && !breakEndDate)) {
        return;
    }
    pill($('body'));
    stop($('body'), populateSchedule);
}

$(document).ready(function() {
    $(ADD_PERSON_BUTTON).on('click', addNewPerson);
    $(SUBMIT_BUTTON).on('click', commit);
});
