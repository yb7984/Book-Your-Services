"""File for function handling google calendar api"""

import datetime
import pytz
import os.path
from google.oauth2 import service_account
from googleapiclient.discovery import build
import config
import os
import json

GOOGLE_CALENDAR_SCOPES = ['https://www.googleapis.com/auth/calendar']
GOOGLE_SERVICE_ACCOUNT_KEY = config.GOOGLE_SERVICE_ACCOUNT_KEY
GOOGLE_SERVICE_ACCOUNT_FILE = config.GOOGLE_SERVICE_ACCOUNT_FILE
GOOGLE_CALENDAR_DEFAULT_TIMEZONE = config.DEFAULT_TIMEZONE

google_calendar_service = None

class GoogleCalendarHandler:
    """Class including methods handling google calendar"""

    @staticmethod
    def format_datetime(datetime_str):
        """Return a formatted datetime string for google calendar use"""

        time_value = datetime.datetime.fromisoformat(datetime_str)

        # adding timezone info to datetime
        time_value = pytz.timezone(GOOGLE_CALENDAR_DEFAULT_TIMEZONE).localize(time_value)

        return time_value.isoformat()

    @staticmethod
    def get_service():
        """return google calendar service api obj"""
        #using the global variable
        global google_calendar_service

        if google_calendar_service is None:
            credentials = None
            info_json = os.environ.get(GOOGLE_SERVICE_ACCOUNT_KEY , None)

            if info_json is not None:
                service_account_info = json.load(info_json)
                credentials = service_account.Credentials.from_service_account_info(service_account_info , 
                scopes=GOOGLE_CALENDAR_SCOPES)
            else :
                credentials = service_account.Credentials.from_service_account_file(
                    GOOGLE_SERVICE_ACCOUNT_FILE,
                    scopes=GOOGLE_CALENDAR_SCOPES)

            google_calendar_service = build('calendar', 'v3', credentials=credentials)

        return google_calendar_service

    @staticmethod
    def calendars_list():
        """Return the calendars list"""

        service = GoogleCalendarHandler.get_service()

        calendars = service.calendarList().list(
            showHidden=True, showDeleted=True).execute()
        return calendars.get('items', [])

    @staticmethod
    def calendars_get(calendar_id):
        """Return the calendar"""

        service = GoogleCalendarHandler.get_service()

        return service.calendars().get(calendarId=calendar_id).execute()


    @staticmethod
    def calendars_insert(calendar=None, summary="", time_zone=None, description="", location=""):
        """Create a new calendar"""
        service = GoogleCalendarHandler.get_service()
        if calendar is None or not calendar:
            if len(summary.strip()) > 0:

                calendar = {
                    "summary": summary,
                    "timeZone": time_zone if time_zone else GOOGLE_CALENDAR_DEFAULT_TIMEZONE,
                    "description": description,
                    "location": location
                }

        if calendar:
            calendar = service.calendars().insert(body=calendar).execute()

            return calendar

        return None


    @staticmethod
    def calendars_update(calendar):
        """Update a calendar"""
        service = GoogleCalendarHandler.get_service()

        calendar = service.calendars().update(
            calendarId=calendar["id"], body=calendar).execute()

        return calendar

    @staticmethod
    def calendars_delete(calendar_id):
        """Delete a calendar"""
        service = GoogleCalendarHandler.get_service()

        return service.calendars().delete(calendarId=calendar_id).execute()



    @staticmethod
    def calendars_share(calendar_id, email):
        """Share a calendar to somebody"""
        service = GoogleCalendarHandler.get_service()

        rule = {
            'scope': {
                'type': 'user',
                'value': email,
            },
            'role': 'reader'
        }

        created_rule = service.acl().insert(calendarId=calendar_id, body=rule, sendNotifications=True).execute()

        return created_rule

    @staticmethod
    def calendars_share_delete(calendar_id, email):
        """End sharing a calendar to somebody"""
        service = GoogleCalendarHandler.get_service()

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
                result = service.acl().delete(calendarId=calendar_id , ruleId=rule['id']).execute()


    @staticmethod
    def events_list(
            max_results=10,
            time_min=None,
            time_max=None,
            time_zone=None,
            order_by="startTime",
            calendar_id="primary"):
        """return the events list"""

        if time_zone is None:
            time_zone = GOOGLE_CALENDAR_DEFAULT_TIMEZONE

        if time_min is None:
            time_min = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        else:
            time_min = GoogleCalendarHandler.format_datetime(time_min)

        if time_max is None:
            time_max = datetime.datetime.max.isoformat() + 'Z'
        else:
            time_min = GoogleCalendarHandlerformat_datetime(time_max)

        service = GoogleCalendarHandler.get_service()

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


    @staticmethod
    def events_get(event_id, calendar_id="primary"):
        """Returns an event."""

        service = GoogleCalendarHandler.get_service()

        return service.events().get(calendarId=calendar_id, eventId=event_id).execute()


    @staticmethod
    def events_insert(event, calendar_id="primary"):
        """insert a calendar event"""

        service = GoogleCalendarHandler.get_service()

        return service.events().insert(calendarId=calendar_id, body=event).execute()


    @staticmethod
    def events_update(event, calendar_id="primary"):
        """update a calendar event"""

        service = GoogleCalendarHandler.get_service()

        return service.events().update(calendarId=calendar_id, eventId=event['id'], body=event).execute()


    @staticmethod
    def events_delete(event_id, calendar_id="primary"):
        """Delete an event."""

        service = GoogleCalendarHandler.get_service()

        return service.events().delete(calendarId=calendar_id, eventId=event_id).execute()


    @staticmethod
    def events_build(summary,
                            start, end,
                            time_zone=None,
                            location="",
                            description="",
                            recurrence=[],
                            attendees=[],
                            reminders={}):
        """Put in the information and return a google calendar event dict"""
        if time_zone is None:
            time_zone = GOOGLE_CALENDAR_DEFAULT_TIMEZONE

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
