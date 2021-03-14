from unittest import TestCase
from app import app
from utils import *
from models import *
from secrets import token_urlsafe
from tests.views.test_data import *

# Use test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bookyourservices_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['WTF_CSRF_ENABLED'] = False


db.drop_all()
db.create_all()

class APIAppointmentTest(TestCase):
    """Test class for Appointment API"""

    def setUp(self):
        """Clean up test data and set up some new data"""
        set_test_data(self)

        set_data_appointment(self.provider_username , self.customer_username , self.service_id , 30)

    def tearDown(self):
        """Clean up any faulted transaction."""
        db.session.rollback()

    def test_appointments_list(self):
        """Testing the appointments_list"""

        with app.test_client() as client:
            # not login
            resp = client.get(f"/api/appointments/{self.customer_username}")

            data = resp.get_json()
            
            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data["error"] , "Unauthorized visit!")

            # login as customer
            login_as_customer(self , client)

            resp = client.get(f"/api/appointments/{self.customer_username}")
            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data["total"] , 31 if datetime.datetime.now().hour < 7 else 30)
            self.assertEqual(data["page"] , 1)
            self.assertEqual(data["per_page"] , 12)
            self.assertEqual(data["pages"] , 3)
            self.assertEqual(len(data["items"]) , 12)

            # login as provider
            login_as_provider(self , client)

            resp = client.get(f"/api/appointments/{self.customer_username}")
            data = resp.get_json()
            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data , {})

            resp = client.get(f"/api/appointments/{self.provider_username}")
            data = resp.get_json()
            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data["total"] , 0)
            self.assertEqual(data["page"] , 1)
            self.assertEqual(data["per_page"] , 12)
            self.assertEqual(data["pages"] , 0)
            self.assertEqual(len(data["items"]) , 0)

            resp = client.get(f"/api/appointments/{self.provider_username}?is_provider=1")
            data = resp.get_json()
            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data["total"] , 31 if datetime.datetime.now().hour < 7 else 30)
            self.assertEqual(data["page"] , 1)
            self.assertEqual(data["per_page"] , 12)
            self.assertEqual(data["pages"] , 3)
            self.assertEqual(len(data["items"]) , 12)

    def test_appointments_insert(self):
        """Testing the appointments_insert"""

        with app.test_client() as client:
            post_data = {
                "appointment-provider_username": self.provider_username ,
                "appointment-customer_username" : self.customer_username ,
                "appointment-service_id" : self.service_id ,
                "appointment-service_date" : (datetime.date.today() + datetime.timedelta(days=1)).isoformat() ,
                "appointment-times" : "14:00-15:00" ,
                "appointment-note" : "test note test note"
            }
            # not login 
            resp = client.post("/api/appointments" , data=post_data)

            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data["error"] , "Unauthorized visit!")

            #login as customer
            login_as_customer(self , client)
            resp = client.post("/api/appointments" , data=post_data)

            data = resp.get_json()

            self.assertEqual(resp.status_code , 201)
            self.assertGreater(data["item"]["id"] , 0)
            self.assertEqual(data["item"]["customer_username"] , self.customer_username)

            #login as provider, can make appointment with himself
            login_as_provider(self , client)
            resp = client.post("/api/appointments" , data=post_data)

            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data["error"] , "You are not supposed to book the service from yourself!")

            # service_date times empty

            post_data["appointment-service_date"] = ""
            post_data["appointment-times"] = ""
            resp = client.post("/api/appointments" , data=post_data)

            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            self.assertGreater(len(data["errors"]) , 0)
            self.assertEqual(data["errors"]["service_date"] , ["This field is required."])
            self.assertEqual(data["errors"]["times"] , ["This field is required."])

    def test_appointments_update(self):
        """Testing the appointments_update"""

        with app.test_client() as client:
            post_data = {
                "appointment-provider_username": self.provider_username ,
                "appointment-customer_username" : self.customer_username ,
                "appointment-service_id" : self.service_id ,
                "appointment-service_date" : (datetime.date.today() + datetime.timedelta(days=1)).isoformat() ,
                "appointment-times" : "16:00-17:00" ,
                "appointment-note" : "test note test note"
            }
            # not login 
            resp = client.patch(f"/api/appointments/{self.appointment_id}" , data=post_data)

            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data["error"] , "Unauthorized visit!")

            # login as customer
            login_as_customer(self, client)

            resp = client.patch(f"/api/appointments/{self.appointment_id}" , data=post_data)

            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            
            appointment = Appointment.query.get(self.appointment_id)
            date = datetime.date.today() + datetime.timedelta(days=1)
            self.assertEqual(appointment.start , localize_datetime(datetime.datetime.combine(date , datetime.time(hour=16))))
            self.assertEqual(appointment.end , localize_datetime(datetime.datetime.combine(date, datetime.time(hour=17))))



            # login as provider
            login_as_provider(self, client)

            post_data["appointment-times"] = "18:00-19:00"

            resp = client.patch(f"/api/appointments/{self.appointment_id}" , data=post_data)

            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            
            appointment = Appointment.query.get(self.appointment_id)
            date = datetime.date.today() + datetime.timedelta(days=1)
            self.assertEqual(appointment.start , localize_datetime(datetime.datetime.combine(date , datetime.time(hour=18))))
            self.assertEqual(appointment.end , localize_datetime(datetime.datetime.combine(date, datetime.time(hour=19))))


    def test_appointments_delete(self):
        """Testing the appointments_delete"""

        with app.test_client() as client:
            # not login 
            resp = client.delete(f"/api/appointments/{self.appointment_id}")

            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data["error"] , "Unauthorized visit!")

            # login as customer
            login_as_customer(self, client)

            resp = client.delete(f"/api/appointments/{self.appointment_id}")

            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data , {})
            
            appointment = Appointment.query.get(self.appointment_id)
            self.assertEqual(appointment.is_active , False)