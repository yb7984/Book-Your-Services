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

TESTING = True


class ViewLoginRequiredTest(TestCase):
    """Test class for views require login"""

    def setUp(self):
        """Clean up test data and set up some new data"""
        set_test_data(self)

    def tearDown(self):
        """Clean up any faulted transaction."""
        db.session.rollback()

    def test_dashboard(self):
        """Testing the dashboard"""

        with app.test_client() as client:
            # not login
            resp = client.get("/users/dashboard" , follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Please login first!', html)

            login_as_customer(test_class=self, client=client)

            user = User.query.get(self.customer_username)

            resp = client.get("/users/dashboard" , follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(user.full_name , html)
            self.assertIn('"appointments-list"', html)
            self.assertNotIn('"services-list"', html)

            login_as_provider(test_class=self, client=client)

            user = User.query.get(self.provider_username)
            resp = client.get("/users/dashboard" , follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(user.full_name , html)
            self.assertIn('"appointments-list"', html)
            self.assertIn('"services-list"', html)

    def test_profile(self):
        """Testing the profile"""

        with app.test_client() as client:
            # not login
            resp = client.get("/users/profile" , follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Please login first!', html)

            login_as_customer(test_class=self, client=client)

            user = User.query.get(self.customer_username)

            resp = client.get("/users/profile" , follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(user.full_name , html)
            self.assertNotIn('Calendar Gmail', html)

            login_as_provider(test_class=self, client=client)

            user = User.query.get(self.provider_username)

            resp = client.get("/users/profile" , follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(user.full_name , html)
            self.assertIn('Calendar Gmail', html)

    def test_user_edit(self):
        """Testing the user_edit"""

        with app.test_client() as client:
            # not login
            resp = client.get("/users/edit" , follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Please login first!', html)

            login_as_customer(test_class=self, client=client)

            user = User.query.get(self.customer_username)

            resp = client.get("/users/edit" , follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(user.full_name , html)
            self.assertIn('First Name', html)
            self.assertIn('Last Name', html)

            resp = client.post("/users/edit" , data={
                "username": user.username,
                "password": user.password,
                "first_name" : "fn_edit" ,
                "last_name" : "ln_edit" , 
                "email" : "test@test.test.com", 
                "phone": "8608608600" ,
                "description": "test_description",
                "is_active" : "y"
            } , follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code , 200)
            self.assertIn("Successfully Update Account!" , html)

            user = User.query.get(self.customer_username)
            self.assertEqual(user.first_name , "fn_edit")
            self.assertEqual(user.last_name , "ln_edit")
            self.assertEqual(user.email , "test@test.test.com")
            self.assertEqual(user.phone , "8608608600")
            self.assertEqual(user.description , "test_description")

            # update is_provider
            resp = client.post("/users/edit" , data={
                "username": user.username,
                "password": user.password,
                "first_name" : "fn_edit" ,
                "last_name" : "ln_edit" , 
                "email" : "test@test.test.com", 
                "phone": "8608608600" ,
                "description": "test_description",
                "is_provider": "y",
                "is_active" : "y"
            } , follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code , 200)
            self.assertIn("Successfully Update Account!" , html)

            user = User.query.get(self.customer_username)
            self.assertEqual(user.is_provider , True)


    def test_password_update(self):
        """Testing the password_update"""

        with app.test_client() as client:
            # not login
            resp = client.get("/users/password" , follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Please login first!', html)

            login_as_customer(test_class=self, client=client)

            user = User.query.get(self.customer_username)

            resp = client.get("/users/password" , follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Edit Password" , html)
            self.assertIn('Password', html)
            self.assertIn('Password Confirm', html)

            resp = client.post("/users/password" , data={
                "password": "pwd_update" ,
                "password_confirm": "pwd_update"
            } , follow_redirects=True)

            html = resp.get_data(as_text=True)


            user = User.query.get(self.customer_username)

            self.assertEqual(resp.status_code , 200)
            self.assertIn('Successfully Updated Password!' , html)
            self.assertEqual(check_password_hash(user.password , "pwd_update") , True)

            resp = client.post("/users/password" , data={
                "password": "pwd_update" ,
                "password_confirm": "pwd_update1"
            } , follow_redirects=True)


            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code , 200)
            self.assertIn('Password must match' , html)


    def test_my_services(self):
        """Testing the my_services"""

        with app.test_client() as client:
            # not login
            resp = client.get("/users/myservices" , follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Please login first!', html)

            login_as_customer(test_class=self, client=client)

            user = User.query.get(self.customer_username)

            resp = client.get("/users/myservices" , follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Unauthorized visit!' , html)


            login_as_provider(test_class=self, client=client)
            user = User.query.get(self.provider_username)

            resp = client.get("/users/myservices" , follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('"services-list"' , html)

    def test_my_schedules(self):
        """Testing the my_schedules"""

        with app.test_client() as client:
            # not login
            resp = client.get("/users/myschedules" , follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Please login first!', html)

            login_as_customer(test_class=self, client=client)

            user = User.query.get(self.customer_username)

            resp = client.get("/users/myschedules" , follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Unauthorized visit!' , html)


            login_as_provider(test_class=self, client=client)
            user = User.query.get(self.provider_username)

            resp = client.get("/users/myschedules" , follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('My Weekly Schedules' , html)
            self.assertIn('Specific Dates Schedules' , html)
            self.assertIn('"schedules-list-weekly"' , html)
            self.assertIn('"schedules-list-dates"' , html)

    def test_my_appointments(self):
        """Testing the my_appointments"""

        with app.test_client() as client:
            # not login
            resp = client.get("/users/myappointments" , follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Please login first!', html)

            login_as_customer(test_class=self, client=client)

            user = User.query.get(self.customer_username)

            resp = client.get("/users/myappointments" , follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('My Appointments' , html)
            self.assertIn('"appointments-list"' , html)
            self.assertIn('<h3 class="text-primary">Upcoming</h3>' , html)

            resp = client.get("/users/myappointments?is_past=1" , follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('My Appointments' , html)
            self.assertIn('"appointments-list"' , html)
            self.assertIn('<h3 class="text-primary">Past</h3>' , html)


            login_as_provider(test_class=self, client=client)
            user = User.query.get(self.provider_username)

            resp = client.get("/users/myappointments" , follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Customer Appointments' , html)
            self.assertIn('"appointments-list"' , html)
            self.assertIn('<h3 class="text-primary">Upcoming</h3>' , html)

            resp = client.get("/users/myappointments?is_past=1" , follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Customer Appointments' , html)
            self.assertIn('"appointments-list"' , html)
            self.assertIn('<h3 class="text-primary">Past</h3>' , html)


    def test_provider_appointments(self):
        """Testing the provider_appointments"""

        with app.test_client() as client:
            # not login
            resp = client.get("/users/provider_appointments" , follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Please login first!', html)

            login_as_customer(test_class=self, client=client)

            user = User.query.get(self.customer_username)

            resp = client.get("/users/provider_appointments" , follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Unauthorized visit!' , html)


            login_as_provider(test_class=self, client=client)
            user = User.query.get(self.provider_username)

            resp = client.get("/users/provider_appointments" , follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Provider Appointments' , html)
            self.assertIn('"appointments-list"' , html)
            self.assertIn('<h3 class="text-primary">Upcoming</h3>' , html)


            resp = client.get("/users/provider_appointments?is_past=1" , follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Provider Appointments' , html)
            self.assertIn('"appointments-list"' , html)
            self.assertIn('<h3 class="text-primary">Past</h3>' , html)


