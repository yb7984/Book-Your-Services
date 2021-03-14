from unittest import TestCase
import json
from google_calendar.google_calendar import *
import datetime

class GoogleCalendarTest(TestCase):
    """Test class for Google Calendar"""
    @classmethod
    def setUpClass(cls):
        """Create a new calendar to test"""

        list = GoogleCalendarHandler.calendars_list()

        for calendar in list:
            print(calendar)
            if calendar['summary'] == 'test calendar':
                cls.calendar_id = calendar.get('id')

                return 
                
        # if not found the test calendar create one

        print ("#####create one")
        calendar = GoogleCalendarHandler.calendars_insert(summary="test calendar" , description="test calendar description")
        cls.calendar_id = calendar.get('id')

    @classmethod
    def tearDownClass(cls):
        """Delete the calendar"""

        # calendar_calendars_delete(cls.calendar_id)

    def setUp(self):
        """Before the test."""

    def tearDown(self):
        """Clean up test data"""

    def test_calendars_list(self):
        """test calendar_calendars_list"""

        list = GoogleCalendarHandler.calendars_list()

        str = json.dumps(list)

        self.assertIn(self.calendar_id , str) 
        self.assertIn("test calendar" , str)

    def test_calendars_get(self):
        """test calendar_calendars_get"""

        calendar = GoogleCalendarHandler.calendars_get(self.calendar_id)

        self.assertEqual(self.calendar_id , calendar['id']) 
        self.assertEqual("test calendar" , calendar['summary'])


    def test_calendars_update(self):
        """test calendar_calendars_update"""

        calendar = GoogleCalendarHandler.calendars_get(self.calendar_id)

        calendar['summary'] = 'test calendar updated'
        calendar['description'] = 'test calendar description updated'

        calendar = GoogleCalendarHandler.calendars_update(calendar)

        calendar = GoogleCalendarHandler.calendars_get(self.calendar_id)

        self.assertEqual('test calendar updated' , calendar['summary'])
        self.assertEqual('test calendar description updated' , calendar['description'])

        calendar['summary'] = 'test calendar'
        calendar['description'] = 'test calendar description'

        calendar = GoogleCalendarHandler.calendars_update(calendar)

    def test_calendars_share(self):
        """test calendar_calendars_share"""

        test_email = 'bobowu98@gmail.com'

        rule = GoogleCalendarHandler.calendars_share(self.calendar_id , test_email)

        service = GoogleCalendarHandler.get_service()
        list = service.acl().list(calendarId=self.calendar_id).execute()

        str = json.dumps(list)

        self.assertIn(self.calendar_id , str)
        self.assertIn(test_email , str)


        GoogleCalendarHandler.calendars_share_delete(calendar_id=self.calendar_id , email=test_email)

        list = service.acl().list(calendarId=self.calendar_id).execute()

        str = json.dumps(list)

        self.assertNotIn(test_email , str)

    def test_events(self):
        """test calendar_events_*"""

        event = GoogleCalendarHandler.events_build(
            summary="test event" , 
            start=datetime.datetime.fromisoformat('2021-01-31T12:32:32') ,
            end=datetime.datetime.fromisoformat('2021-01-31T14:30:30') ,
            location='test location' ,
            description='test description')

        event = GoogleCalendarHandler.events_insert(event , calendar_id=self.calendar_id)

        event_id = event.get('id' , None)
        #successfully insert and the id is not None
        self.assertIsNotNone(event_id)

        event = GoogleCalendarHandler.events_get(event_id=event_id , calendar_id=self.calendar_id)

        self.assertEqual('test event' , event.get('summary'))

        list = GoogleCalendarHandler.events_list(calendar_id=self.calendar_id , time_min='2021-01-30')

        str = json.dumps(list)

        self.assertIn('test event' , str)

        #update
        event['summary']    = 'test event updated'

        GoogleCalendarHandler.events_update(event , calendar_id=self.calendar_id)

        event = GoogleCalendarHandler.events_get(event_id=event_id , calendar_id=self.calendar_id)

        self.assertEqual('test event updated' , event.get('summary'))

        #delete the event 
        GoogleCalendarHandler.events_delete(event_id , calendar_id=self.calendar_id)

        event = GoogleCalendarHandler.events_get(event_id=event_id , calendar_id=self.calendar_id)

        #status change to cancelled
        self.assertEqual(event.get('status') , 'cancelled')




