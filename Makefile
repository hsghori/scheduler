all:
	browserify static/js/main.js > static/js/bundle.js
	sass static/scss/base.scss static/css/main.css
