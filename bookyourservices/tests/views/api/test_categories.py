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


class APICategoryTest(TestCase):
    """Test class for Category API"""

    def setUp(self):
        """Clean up test data and set up some new data"""
        set_test_data(self)

        set_data_categories(5)

    def tearDown(self):
        """Clean up any faulted transaction."""
        db.session.rollback()

    def test_categories_list(self):
        """Testing the categories_list"""

        with app.test_client() as client:
            category = Category.query.get(self.category_id)
            category.is_active = False

            db.session.commit()

            resp = client.get("/api/categories")

            data = resp.get_json()

            self.assertEqual(resp.status_code, 200)

            # not login only return active categories
            self.assertEqual(len(data["items"]), 5)

            # customer
            login_as_customer(self, client)
            resp = client.get("/api/categories")

            data = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            # customer only return active categories
            self.assertEqual(len(data["items"]), 5)

            # provider
            login_as_provider(self, client)
            resp = client.get("/api/categories")

            data = resp.get_json()

            self.assertEqual(resp.status_code, 200)

            # provider only return active categories
            self.assertEqual(len(data["items"]), 5)

            # admin
            login_as_admin(self, client)


            resp = client.get("/api/categories")

            data = resp.get_json()

            self.assertEqual(resp.status_code, 200)

            # admin return all categories
            self.assertEqual(len(data["items"]), 6)

    def test_categories_insert(self):
        """Testing the categories_insert"""

        with app.test_client() as client:

            post_data = {
                "name": "test_category"
            }
            # not login
            resp = client.post("/api/categories", data=post_data)

            data = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data["error"], "Unauthorized visit!")

            # customer can't insert service
            login_as_customer(self, client)
            resp = client.post("/api/categories", data=post_data)

            data = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data, {"error": "Unauthorized visit!"})

            # provider
            login_as_provider(self, client)

            resp = client.post("/api/categories", data=post_data)

            data = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data, {"error": "Unauthorized visit!"})


            # admin
            login_as_admin(self, client)

            resp = client.post("/api/categories", data=post_data)
            
            data = resp.get_json()

            self.assertEqual(resp.status_code, 201)
            self.assertGreater(data["item"]["id"], 0)
            self.assertEqual(data["item"]["name"], "test_category")

            # name no value, return errors
            post_data["name"] = ""
            resp = client.post("/api/categories", data=post_data)

            data = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data["errors"], {"name": ["This field is required."]})

    
    def test_categories_update(self):
        """Testing the categories_update"""

        with app.test_client() as client:

            post_data = {
                "name": "test_category_update" , 
                "is_active": 'y'
            }
            # not login
            resp = client.patch(f"/api/categories/{self.category_id}", data=post_data)

            data = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data["error"], "Unauthorized visit!")

            # customer can't insert service
            login_as_customer(self, client)
            resp = client.patch(f"/api/categories/{self.category_id}", data=post_data)

            data = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data, {"error": "Unauthorized visit!"})

            # provider
            login_as_provider(self, client)

            resp = client.patch(f"/api/categories/{self.category_id}", data=post_data)

            data = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data, {"error": "Unauthorized visit!"})


            # admin
            login_as_admin(self, client)

            resp = client.patch(f"/api/categories/{self.category_id}", data=post_data)
            
            data = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data["item"]["name"], "test_category_update")

            # name no value, return errors
            post_data["name"] = ""
            resp = client.patch(f"/api/categories/{self.category_id}", data=post_data)

            data = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data["errors"], {"name": ["This field is required."]})

    def test_categories_delete(self):
        """Testing the categories_delete"""

        with app.test_client() as client:

            # not login
            resp = client.delete(f"/api/categories/{self.category_id}")

            data = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data["error"], "Unauthorized visit!")

            # customer can't insert service
            login_as_customer(self, client)
            resp = client.delete(f"/api/categories/{self.category_id}")

            data = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data, {"error": "Unauthorized visit!"})

            # provider
            login_as_provider(self, client)
            resp = client.delete(f"/api/categories/{self.category_id}")

            data = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data, {"error": "Unauthorized visit!"})


            # admin
            login_as_admin(self, client)
            resp = client.delete(f"/api/categories/{self.category_id}")
            
            data = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            
            category = Category.query.get(self.category_id)

            self.assertEqual(category.is_active , False)

