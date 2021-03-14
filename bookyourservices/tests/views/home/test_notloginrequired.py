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



class ViewNoLoginTest(TestCase):
    """Test class for views not require login"""

    def setUp(self):
        """Clean up test data and set up some new data"""
        set_test_data(self)

    def tearDown(self):
        """Clean up any faulted transaction."""
        db.session.rollback()

    def test_index(self):
        """Testing the index"""

        with app.test_client() as client:
            resp = client.get("/")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code , 200)
            self.assertIn('<a class="nav-link text-success" href="/register">Register</a>' , html)
            self.assertIn('<a class="nav-link text-success" href="/login">Login</a>' , html)
            self.assertIn("Services" , html)
            self.assertIn("Providers" , html)
            self.assertIn('id="services-list"' , html)
            self.assertIn('id="providers-list"' , html)

            login_as_customer(test_class=self , client=client)

            resp = client.get("/")

            html = resp.get_data(as_text=True)

            self.assertIn(self.customer.full_name , html)
            self.assertNotIn('<a class="nav-link text-success" href="/register">Register</a>' , html)
            self.assertNotIn('<a class="nav-link text-success" href="/login">Login</a>' , html)


    def test_services_list(self):
        """Testing the services_list"""

        with app.test_client() as client:
            resp = client.get("/services")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code , 200)
            self.assertIn("Services" , html)
            self.assertIn('id="services-list"' , html)


            resp = client.get(f"/services?term=searchtest&categories={self.category.id}")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code , 200)
            self.assertIn('value="searchtest"' , html)
            self.assertIn(f'selected value="{self.category.id}"' , html)

    def test_providers_list(self):
        """Testing the services_list"""

        with app.test_client() as client:
            resp = client.get("/providers")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code , 200)
            self.assertIn("Providers" , html)
            self.assertIn('id="providers-list"' , html)

            resp = client.get("/providers?term=searchtest")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code , 200)
            self.assertIn('value="searchtest"' , html)