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


class ViewUserTest(TestCase):
    """Test class for views for user information"""

    def setUp(self):
        """Clean up test data and set up some new data"""
        set_test_data(self)

    def tearDown(self):
        """Clean up any faulted transaction."""
        db.session.rollback()

    def test_login(self):
        """Testing the login"""

        with app.test_client() as client:
            resp = client.get("/login")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('User Login', html)
            self.assertIn('Username', html)
            self.assertIn("Password", html)
            self.assertIn("Forgot the password", html)

            # post the login information incorrectly
            resp = client.post("/login", data={
                "username": self.customer.username,
                "password": "test1"
            }, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"Invalid username/password", html)

            # post the login information correctly
            resp = client.post("/login", data={
                "username": self.customer.username,
                "password": "test"
            }, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"Welcome Back, {self.customer.full_name}!", html)

            # already login redirect
            login_as_customer(test_class=self, client=client)

            resp = client.get("/login")

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/users/dashboard")

    def test_register(self):
        """Testing the register"""

        with app.test_client() as client:
            resp = client.get("/register")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('User Register', html)
            self.assertIn('Username', html)
            self.assertIn('Password', html)
            self.assertIn('Email', html)
            self.assertIn('Email for Google Calendar', html)

            # post duplicate username / email

            resp = client.post("/register", data={
                "username": self.customer.username,
                "password": "test",
                "email": self.customer.email
            })

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Username taken.', html)
            self.assertIn('Email taken.', html)

            # post username / email
            resp = client.post("/register", data={
                "username": "testuser",
                "password": "test",
                "email": "test@ybdevs.com"
            }, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Successfully Registered!', html)

    def test_password_reset(self):
        """Testing the password_reset"""

        with app.test_client() as client:
            resp = client.get("/password_reset")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Reset Password', html)
            self.assertIn('Email', html)
            self.assertIn('Input your email with your account here', html)

            # email exists
            resp = client.post("/password_reset", data={
                "email": self.customer.email
            }, follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("The reset email has been sent to you email address!" , html)

            # email not exist
            resp = client.post("/password_reset", data={
                "email": 'test@tes.com'
            }, follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Email is not found!" , html)


            user = User.query.get(self.customer.username)

            # invalid token
            resp = client.get(f"/password_reset?token={user.pwd_token}1" , follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Invalid Token, please try again!" , html)

            # right token
            resp = client.get(f"/password_reset?token={user.pwd_token}")

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("New Password" , html)

            # update new password
            resp = client.post(f"/password_reset?token={user.pwd_token}", data={
                "password": "test2"
            }, follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Successfully reset password!" , html)


            user = User.query.get(self.customer.username)
            self.assertEqual(user.pwd_token , '')
            self.assertEqual(check_password_hash(user.password , "test2") , True)

    def test_logout(self):
        """Testing the logout"""

        with app.test_client() as client:

            login_as_customer(self , client)

            resp = client.post("/logout" , follow_redirects=True)

            self.assertEqual(resp.status_code , 200)
            self.assertEqual(session.get(USERNAME_SESSION_KEY) , None)