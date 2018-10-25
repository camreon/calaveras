from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from flask import Flask, render_template
import random
import os

SCOPE = 'https://www.googleapis.com/auth/spreadsheets.readonly'
API_KEY = os.environ['API_KEY']
SPREADSHEET_ID = os.environ['SPREADSHEET_ID']
RANGE_NAME = os.environ['RANGE_NAME']

app = Flask(__name__)

@app.route("/")
def index():
    service = build('sheets', 'v4', developerKey=API_KEY)

    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                range=RANGE_NAME).execute()
    values = result.get('values', [])
    value = random.choice(values)

    calevara = value[1] if len(value) > 1 else 'default calevara'
    name = value[2] if len(value) > 2 else 'sam'
    agency = value[3] if len(value) > 3 else 'wondroman'

    return render_template('index.html', calevara=calevara, name=name, agency=agency)

@app.route("/create/")
def create():
    return render_template('create.html')

@app.route("/create-new/")
def create_new():
    return render_template('create_new.html')

@app.route("/create-mad-lib/")
def create_mad_lib():
    return render_template('create_mad_lib.html')

@app.route("/submitted/")
def submitted():
    return render_template('submitted.html')
