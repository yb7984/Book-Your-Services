from flask import Blueprint, render_template , g , request
from google_calendar.google_calendar import *

home = Blueprint('home', __name__)

@home.route('/')
def index():
    # Do some stuff

    events = calendar_events_list(time_min='2020-12-01T00:00:00' , max_results=20)

    html = ''
    if not events:
        return 'No upcoming events found.'
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        html += start + event['summary'] + "<br/>"
    return render_template("home/index.html" , html=html)