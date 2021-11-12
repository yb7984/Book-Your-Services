from unittest import TestCase
from app import app
from utils import *
from models import *
from secrets import token_urlsafe
from tests.views.test_data import *


from tests.test_common import test_setup

test_setup(app=app , db=db)

TESTING = True


class ViewAdminCategoryTest(TestCase):
    """Test class for views for category data"""

    def setUp(self):
        """Clean up test data and set up some new data"""
        set_test_data(self)

    def tearDown(self):
        """Clean up any faulted transaction."""
        db.session.rollback()


    def test_categories_index(self):
        """Testing the categories_index"""
        with app.test_client() as client:
            resp = client.get("/admin/categories/index")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertIn("http://localhost/admin/login" ,resp.location)


            login_as_provider(self , client)
            resp = client.get("/admin/categories/index")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertIn("http://localhost/admin/login" ,resp.location)

            login_as_admin(self, client)

            resp = client.get("/admin/categories/index")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('All Categories', html)
            self.assertIn('id="categories-list"', html)

