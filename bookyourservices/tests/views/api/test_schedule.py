from unittest import TestCase
from app import app
from utils import *
from models import *
from secrets import token_urlsafe
from tests.views.test_data import *
from datetime import date, timedelta

# Use test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bookyourservices_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['WTF_CSRF_ENABLED'] = False


db.drop_all()
db.create_all()

class APIScheduleTest(TestCase):
    """Test class for Schedule API"""

    def setUp(self):
        """Clean up test data and set up some new data"""
        set_test_data(self)

        set_data_schedule(self.provider_username)

    def tearDown(self):
        """Clean up any faulted transaction."""
        db.session.rollback()

    def test_schedules_list(self):
        """Testing the schedules_list"""

        with app.test_client() as client:
            resp = client.get(f"/api/schedules/{self.provider_username}/weekly")

            data = resp.get_json()
            
            self.assertEqual(resp.status_code , 200)
            self.assertEqual(len(data["items"]) , 5)

            resp = client.get(f"/api/schedules/{self.provider_username}/dates")

            data = resp.get_json()
            
            self.assertEqual(resp.status_code , 200)
            self.assertEqual(len(data["items"]) , 0)

    def test_schedules_list_available_times(self):
        """Testing the schedules_list_available_times"""

        with app.test_client() as client:
            # insert only 2 times available
            appointment = Appointment.query.get(self.appointment_id)
            resp = client.get(f"/api/schedules/{self.provider_username}/{appointment.start.date().isoformat()}/0")

            data = resp.get_json()
            print(appointment)
            print(data)
            self.assertEqual(resp.status_code , 200)
            self.assertEqual(len(data["items"]) , 2)

            # update 3 times available
            appointment = Appointment.query.get(self.appointment_id)
            resp = client.get(f"/api/schedules/{self.provider_username}/{appointment.start.date().isoformat()}/{self.appointment_id}")

            data = resp.get_json()
            
            self.assertEqual(resp.status_code , 200)
            self.assertEqual(len(data["items"]) , 3)

    def test_schedules_update(self):
        """Testing the schedules_update"""

        with app.test_client() as client:

            date1 = date.today() + timedelta(days=1)
            date2 = date.today() + timedelta(days=3)

            post_data = {
                "schedule-date_exp_weekly":["1","2"] ,
                "schedule-date_exp_dates":f"{date1.isoformat()},{date2.isoformat()}",
                "schedule-schedules":"",
                "schedule-is_active":"y",
                "schedule-schedules-start": "07:00,08:00",
                "schedule-schedules-end": "08:00,10:00"
            }

            # not login 
            
            resp = client.post(f"/api/schedules/{self.provider_username}" , data=post_data , follow_redirects=True)

            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data["error"] , "Unauthorized visit!")


            # customer can't update schedule
            login_as_customer(self , client)

            resp = client.post(f"/api/schedules/{self.customer_username}" , data=post_data , follow_redirects=True)

            data = resp.get_json()
            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data , {"error" : "Unauthorized visit!"})

            login_as_provider(self , client)

            resp = client.post(f"/api/schedules/{self.provider_username}" , data=post_data , follow_redirects=True)

            data = resp.get_json()
            
            self.assertEqual(resp.status_code , 200)
            self.assertEqual(len(data["items"]) , 4) # got 4 schedules updated

            schedules = Schedule.query.filter(
                Schedule.username==self.provider_username , 
                Schedule.date_exp.in_(['1' , '2' , date1.isoformat(),date2.isoformat()])).all()

            self.assertEqual(len(schedules) , 4)
            self.assertEqual(schedules[0].schedules , schedules[1].schedules)
            self.assertEqual(schedules[0].schedules , schedules[2].schedules)
            self.assertEqual(schedules[0].schedules , schedules[3].schedules)

    def test_schedules_delete(self):
        """Testing the schedules_delete"""

        with app.test_client() as client:
            # not login 
            
            resp = client.delete(f"/api/schedules/{self.provider_username}/1")

            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data["error"] , "Unauthorized visit!")


            # customer can't update schedule
            login_as_customer(self , client)

            resp = client.delete(f"/api/schedules/{self.provider_username}/1")

            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data , {"error" : "Unauthorized visit!"})

            login_as_provider(self , client)

            resp = client.delete(f"/api/schedules/{self.provider_username}/1")

            data = resp.get_json()
            
            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data , {})

            schedules = Schedule.query.filter(
                Schedule.username==self.provider_username , 
                Schedule.date_exp=="1").all()

            self.assertEqual(len(schedules) , 0)



