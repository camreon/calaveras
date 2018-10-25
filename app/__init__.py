from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from flask import Flask, render_template, request, session
import random
import os

SCOPE = 'https://www.googleapis.com/auth/spreadsheets.readonly'
API_KEY = os.environ['API_KEY']
SPREADSHEET_ID = os.environ['SPREADSHEET_ID']
RANGE_NAME = os.environ['RANGE_NAME']  # should always be 'Form Responses!A2:E' if using the default sheet created by Google Forms

# madlibs are formatted as follows:
#   - the text has sequential numbers wherever the user should fill in a word
#   - the expected inputs are listed in order by their part of speech (the listed part of speech is displayed in the input form too)
MADLIBS = [
    {
        'text': 'Eureka! But wait, I check Google. I discover—and ain’t it my luck— My concept’’s been done by a junior named “Dougal,” At 1, that smug little 2.',
        'inputs': ['NOUN', 'NOUN']
    },
    {
        'text': '1 was going viral And I wanted on that train. Comps sent me down a stock spiral Now, to me, 2 just means pain.',
        'inputs': ['NOUN', 'NOUN']
    },
    {
        'text': 'One day, I had a thought: Right now 1 are hot. I pitched it to my team Who promptly killed my dream.',
        'inputs': ['PLURAL NOUN']
    }
]

app = Flask(__name__)
app.secret_key = API_KEY

@app.route("/")
def index():
    service = build('sheets', 'v4', developerKey=API_KEY)

    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                range=RANGE_NAME).execute()
    values = result.get('values', [])
    value = random.choice(values)

    calavera = None
    name = None
    agency = None

    if len(value) > 1:
        calavera = value[1]
        name = value[2] if len(value) > 2 else None
        agency = value[3] if len(value) > 3 else None

    return render_template('index.html', calavera=calavera, name=name, agency=agency)

@app.route("/create/")
def create():
    return render_template('create.html')

@app.route("/create-new/")
def create_new():
    return render_template('create_new.html')

@app.route("/create-mad-lib/")
def create_mad_lib():
    madlib = random.choice(MADLIBS)

    session['madlib'] = madlib['text']
    expected_inputs = madlib['inputs']

    return render_template('create_mad_lib.html', expected_inputs=expected_inputs)

@app.route("/finish-mad-lib/")
def finish_mad_lib():
    madlib = session['madlib'] if 'madlib' in session else ''
    inputs = request.args
    
    for placeholder, user_input in inputs.items():
        madlib = madlib.replace(placeholder, user_input, 1)

    return render_template('finish_mad_lib.html', madlib=madlib)

@app.route("/submitted/")
def submitted():
    return render_template('submitted.html')
