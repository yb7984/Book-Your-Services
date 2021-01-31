"""File for function handling google calendar api"""

import datetime
import pytz
import os.path
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'service.json'
DEFAULT_TIMEZONE = 'America/New_York'

calendar_service = None


def calendar_format_datetime(datetime_str):
    """Return a formatted datetime string for google calendar use"""

    time_value = datetime.datetime.fromisoformat(datetime_str)

    # adding timezone info to datetime
    time_value = pytz.timezone(DEFAULT_TIMEZONE).localize(time_value)

    return time_value.isoformat()


def calendar_get_service():
    """return google calendar service api obj"""
    #using the global variable
    global calendar_service

    if calendar_service is None:

        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=SCOPES)

        calendar_service = build('calendar', 'v3', credentials=credentials)

    return calendar_service


def calendar_calendars_list():
    """Return the calendars list"""

    service = calendar_get_service()

    calendars = service.calendarList().list(
        showHidden=True, showDeleted=True).execute()
    return calendars.get('items', [])


def calendar_calendars_insert(calendar=None, summary="", time_zone=None, description="", location=""):
    """Create a new calendar"""
    service = calendar_get_service()
    if calendar is None or not calendar:
        if len(summary.strip()) > 0:

            calendar = {
                "summary": summary,
                "timeZone": time_zone if time_zone else DEFAULT_TIMEZONE,
                "description": description,
                "location": location
            }

    if calendar:
        calendar = service.calendars().insert(body=calendar).execute()

        return calendar

    return None


def calendar_calendars_update(calendar):
    """Update a calendar"""
    service = calendar_get_service()

    calendar = service.calendars().update(
        calendarId=calendar["id"], body=calendar).execute()

    return calendar


def calendar_calendars_delete(calendar_id):
    """Delete a calendar"""
    service = calendar_get_service()

    return service.calendars().delete(calendarId=calendar_id).execute()

# def calendar_calendars_clear(calendar_id):
#     """Delete all the event of the calendar"""
#     service = calendar_get_service()

#     service.calendars().clear(calendarId=calendar_id).execute()


def calendar_calendars_share(calendar_id, email):
    """Share a calendar to somebody"""
    service = calendar_get_service()

    rule = {
        'scope': {
            'type': 'user',
            'value': email,
        },
        'role': 'reader'
    }

    created_rule = service.acl().insert(calendarId=calendar_id, body=rule,
                                        sendNotifications=True).execute()

    return created_rule

def calendar_calendars_share_delete(calendar_id, email):
    """End sharing a calendar to somebody"""
    service = calendar_get_service()

    rule = {
        'scope': {
            'type': 'user',
            'value': email,
        },
        'role': 'reader'
    }

    list = service.acl().list(calendarId=calendar_id).execute()

    for rule in list.get('items' , []):
        if rule.get('scope' , {}).get('value' , '') == email:
            service.acl().delete(calendarId=calendar_id , ruleId=rule.get('id'))


def calendar_events_list(
        max_results=10,
        time_min=None,
        time_max=None,
        time_zone=None,
        order_by="startTime",
        calendar_id="primary"):
    """return the events list"""

    if time_zone is None:
        time_zone = DEFAULT_TIMEZONE

    if time_min is None:
        time_min = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    else:
        time_min = calendar_format_datetime(time_min)

    if time_max is None:
        time_max = datetime.datetime.max.isoformat() + 'Z'
    else:
        time_min = calendar_format_datetime(time_max)

    service = calendar_get_service()

    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=time_min,
        timeMax=time_max,
        maxResults=max_results,
        timeZone=time_zone,
        singleEvents=True,
        orderBy=order_by
    ).execute()
    return events_result.get('items', [])


def calendar_events_get(event_id, calendar_id="primary"):
    """Returns an event."""

    service = calendar_get_service()

    return service.events().get(calendarId=calendar_id, eventId=event_id).execute()


def calendar_events_insert(event, calendar_id="primary"):
    """insert a calendar event"""

    service = calendar_get_service()

    return service.events().insert(calendarId=calendar_id, body=event).execute()


def calendar_events_update(event, calendar_id="primary"):
    """update a calendar event"""

    service = calendar_get_service()

    return service.events().update(calendarId=calendar_id, eventId=event['id'], body=event).execute()


def calendar_events_delete(event_id, calendar_id="primary"):
    """Delete an event."""

    service = calendar_get_service()

    return service.events().delete(calendarId=calendar_id, eventId=event_id).execute()


def calendar_events_build(summary,
                          start, end,
                          time_zone=None,
                          location="",
                          description="",
                          recurrence=[],
                          attendees=[],
                          reminders={}):
    """Put in the information and return a google calendar event dict"""
    if time_zone is None:
        time_zone = DEFAULT_TIMEZONE

    return {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start.isoformat(),
            'timeZone': time_zone,
        },
        'end': {
            'dateTime': end.isoformat(),
            'timeZone': time_zone,
        },
        'recurrence': recurrence,
        'attendees': attendees,
        'reminders': reminders,
    }
