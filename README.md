### Mad Lib Calaveras

Flask web app that uses Google Sheets as a kind of database by writing to the sheet using a hidden Google Form and reading from the sheet using the Sheets API.

The 3 madlibs and their expected inputs are hardcoded in `__init__.py` for now

# Setup

- Create a Google Form
- In `templates/create_new.html` and `finish_mad_lib.html`, set the form action to the same as the Google Form action and set the input names to the Google Form input names as well
- Create Google Sheets API key https://developers.google.com/sheets/api/guides/authorizing
- Create `.env` file and include config vars
- Run `heroku local`


# Deployment

- Heroku is auto deploying from this repo's master branch for now
- Required config vars are `API_KEY`, `RANGE_NAME`, and `SPREADSHEET_ID`


# Todo

- Add CSS and style all the templates
- Pull madlibs and expected inputs from a set column in the Google Sheet
- Create a madlib object and refactor