from unittest import TestCase
from app import app
from utils import *
from models import *
from secrets import token_urlsafe
from tests.views.test_data import *


from tests.test_common import test_setup

test_setup(app=app , db=db)


class APIProviderTest(TestCase):
    """Test class for provider API"""

    def setUp(self):
        """Clean up test data and set up some new data"""
        set_test_data(self)

        set_data_providers(30)

    def tearDown(self):
        """Clean up any faulted transaction."""
        db.session.rollback()

    def test_schedules_list(self):
        """Testing the schedules_list"""

        with app.test_client() as client:
            resp = client.get(f"/api/providers")

            data = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data["total"], 31)
            self.assertEqual(data["page"], 1)
            self.assertEqual(data["per_page"], 20)
            self.assertEqual(data["pages"], 2)
            self.assertEqual(len(data["items"]), 20)

            resp = client.get("/api/providers?page=2")

            data = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data["total"], 31)
            self.assertEqual(data["page"], 2)
            self.assertEqual(data["per_page"], 20)
            self.assertEqual(data["pages"], 2)
            self.assertEqual(len(data["items"]), 11)

            resp = client.get("/api/providers?limit=12")

            data = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data["total"], 31)
            self.assertEqual(data["page"], 1)
            self.assertEqual(data["per_page"], 12)
            self.assertEqual(data["pages"], 3)
            self.assertEqual(len(data["items"]), 12)

            resp = client.get("/api/providers?term=12")

            data = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data["total"], 1)
            self.assertEqual(len(data["items"]), 1)
            found = (
                ("12" in data["items"][0]["username"]) or
                ("12" in data["items"][0]["first_name"]) or 
                ("12" in data["items"][0]["last_name"]) or 
                ("12" in data["items"][0]["email"]) or 
                ("12" in data["items"][0]["description"])
            )
            self.assertEqual(found , True)

            resp = client.get("/api/providers?email=12")

            data = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data["total"], 1)
            self.assertEqual(len(data["items"]), 1)
            self.assertIn("12", data["items"][0]["email"])
