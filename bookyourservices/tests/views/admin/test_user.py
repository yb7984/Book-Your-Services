from unittest import TestCase
from app import app
from utils import *
from models import *
from secrets import token_urlsafe
from tests.views.test_data import *


from tests.test_common import test_setup

test_setup(app=app , db=db)

class ViewAdminUserTest(TestCase):
    """Test class for views for admin data"""

    def setUp(self):
        """Clean up test data and set up some new data"""
        set_test_data(self)

    def tearDown(self):
        """Clean up any faulted transaction."""
        db.session.rollback()


    def test_users_list(self):
        """Testing the users_list"""
        with app.test_client() as client:
            resp = client.get("/admin/users")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertIn("http://localhost/admin/login" ,resp.location)


            login_as_provider(self , client)
            resp = client.get("/admin/users")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertIn("http://localhost/admin/login" ,resp.location)

            login_as_admin(self, client)

            resp = client.get("/admin/users")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Users List', html)
            self.assertIn(self.customer_username, html)
            self.assertIn(self.provider_username, html)

    def test_users_get(self):
        """Testing the users_get"""
        with app.test_client() as client:
            customer = User.query.get(self.customer_username)
            provider = User.query.get(self.provider_username)

            resp = client.get(f"/admin/users/{self.customer_username}")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertIn("http://localhost/admin/login" ,resp.location)


            login_as_provider(self , client)
            resp = client.get(f"/admin/users/{self.customer_username}")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertIn("http://localhost/admin/login" ,resp.location)

            login_as_admin(self, client)

            resp = client.get(f"/admin/users/{self.customer_username}")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('User:', html)
            self.assertIn(customer.username, html)
            self.assertIn('id="appointments"', html)
            self.assertNotIn('id="schedules"', html)
            self.assertNotIn('id="services"', html)

            resp = client.get(f"/admin/users/{self.provider_username}")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('User:', html)
            self.assertIn(provider.username, html)
            self.assertIn('id="schedules"', html)
            self.assertIn('id="services"', html)
            self.assertIn('id="appointments"', html)


    def test_users_new(self):
        """Testing the users_new"""

        with app.test_client() as client:
            resp = client.get("/admin/users/new")

            self.assertEqual(resp.status_code , 302)
            self.assertIn("http://localhost/admin/login" , resp.location)


            login_as_admin(self , client)

            resp = client.get("/admin/users/new")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('New User', html)

            # post duplicate username / email
            user = User.query.get(self.customer_username)

            post_data= {
                "username": user.username,
                "password": "test",
                "email": user.email,
                "first_name":"f_test",
                "last_name":"l_test",
                "phone": "",
                "description":""
            }

            resp = client.post("/admin/users/new", data=post_data)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Username taken', html)
            self.assertIn('Email taken', html)

            # post username / email

            post_data["username"] = "testuser"
            post_data["email"] = "test@ybdevs.com"
            resp = client.post("/admin/users/new", data=post_data, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Successfully Created New User!', html)

    def test_users_update(self):
        """Testing the users_update"""

        with app.test_client() as client:

            customer = User.query.get(self.customer_username)
            provider = User.query.get(self.provider_username)

            resp = client.get(f"/admin/users/{customer.username}/update")

            self.assertEqual(resp.status_code , 302)
            self.assertIn("http://localhost/admin/login" , resp.location)


            login_as_admin(self , client)

            resp = client.get(f"/admin/users/{customer.username}/update")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edit User', html)
            self.assertIn(customer.username , html)

            # post duplicate email
            post_data= {
                "username": customer.username,
                "password": "test",
                "email": provider.email,
                "first_name":"f_test",
                "last_name":"l_test",
                "phone": "",
                "description":""
            }

            resp = client.post(f"/admin/users/{customer.username}/update", data=post_data , follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Email taken', html)

            # post username / email

            post_data["email"] = "test@ybdevs.com"
            resp = client.post(f"/admin/users/{customer.username}/update", data=post_data, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Successfully Update User!', html)

    def test_users_delete(self):
        """Testing the users_delete"""

        with app.test_client() as client:

            resp = client.post(f"/admin/users/{self.customer_username}/delete")

            self.assertEqual(resp.status_code , 302)
            self.assertIn("http://localhost/admin/login" , resp.location)


            login_as_admin(self , client)

            resp = client.post(f"/admin/users/{self.customer_username}/delete", follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Successfull deactivate an user account!" , html)

