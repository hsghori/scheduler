const createForm = (name) => `
	<div class="sd-card sd-elevation-2 individual-form">
	    <div class="row-button-wrapper right">
	        <button class="sd-unbutton js-close-form">X</button>
	    </div>
	    <div id="name"></div>
	    <fieldset>
	        <legend class="sd-form-label">Select all excluded days</legend>
	        <div class="sd-form-field mod-horizontal-layout days-checks">
	            <input id="checkbox_sunday_${name}" type="checkbox" class="sd-form-checkbox" />
	            <label for="checkbox_sunday_${name}" class="sd-form-label">Sunday</label>
	            <input id="checkbox_monday_${name}" type="checkbox" class="sd-form-checkbox" />
	            <label for="checkbox_monday_${name}" class="sd-form-label">Monday</label>
	            <input id="checkbox_tuesday_${name}" type="checkbox" class="sd-form-checkbox" />
	            <label for="checkbox_tuesday_${name}" class="sd-form-label">Tuesday</label>
	            <input id="checkbox_wednesday_${name}" type="checkbox" class="sd-form-checkbox" />
	            <label for="checkbox_wednesday_${name}" class="sd-form-label">Wednesday</label>
	            <input id="checkbox_thursday_${name}" type="checkbox" class="sd-form-checkbox" />
	            <label for="checkbox_thursday_${name}" class="sd-form-label">Thursday</label>
	        </div>
	    </fieldset>
	    <div class="dates js-dates-text-box"></div>
	    <div class="side-by-side">
	        <input type="date" class="js-specific-date" placeholder="Specific dates" multiple></input>
	        <button class="sd-unbutton commit-button js-commit-date">Commit date</button>
	    </div>
	    <button class="js-clear-dates">Clear</button>
	</div>
`;

const DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday'];


module.exports = { createForm, DAYS };