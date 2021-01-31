from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime, timedelta
from google_calendar import *

app = Flask(__name__)

app.config['SECRET_KEY'] = 'soso'



@app.route("/")
def homepage():

    

    list = calendar_calendars_list()

    id = list[0]["id"]

    # calendar_calendars_share(id , "bobowu98@gmail.com")

    event = calendar_events_build(summary='testtest' , start=(datetime.datetime.now() + timedelta(days=3)) , end=(datetime.datetime.now() + timedelta(days=3 , hours=2)))
    event = calendar_events_insert(event , calendar_id=id)


    events = calendar_events_list(time_min='2020-12-01T00:00:00' , max_results=20)

    html = ''
    if not events:
        return 'No upcoming events found.'
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        html += start + event['summary'] + "<br/>"

    # calendar = calendar_calendars_insert("test calendar 1")
    # print(calendar)
    print(calendar_calendars_list())

    return html