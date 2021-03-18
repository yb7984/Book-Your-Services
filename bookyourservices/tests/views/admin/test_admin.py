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


class ViewAdminTest(TestCase):
    """Test class for views for admin information"""

    def setUp(self):
        """Clean up test data and set up some new data"""
        set_test_data(self)

    def tearDown(self):
        """Clean up any faulted transaction."""
        db.session.rollback()

    def test_login(self):
        """Testing the login"""

        with app.test_client() as client:
            resp = client.get("/admin/login")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Admin Login', html)
            self.assertIn('Username', html)
            self.assertIn("Password", html)
            self.assertIn("Forgot the password", html)

            # post the login information incorrectly
            resp = client.post("/admin/login", data={
                "username": self.admin_username,
                "password": "12345"
            }, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"Invalid username/password", html)

            admin = Admin.query.get(self.admin_username)

            # post the login information correctly
            resp = client.post("/admin/login", data={
                "username": self.admin_username,
                "password": "1234"
            }, follow_redirects=False)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location , "http://localhost/admin")

            # already login redirect
            login_as_admin(test_class=self, client=client)

            resp = client.get("/admin/login")

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/admin")

    def test_logout(self):
        """Testing the logout"""

        with app.test_client() as client:

            login_as_admin(self , client)

            resp = client.post("/admin/logout" , follow_redirects=True)

            self.assertEqual(resp.status_code , 200)
            self.assertEqual(session.get(ADMIN_USER_SESSION_KEY) , None)


    def test_admin_list(self):
        """Testing the admin list"""
        with app.test_client() as client:
            resp = client.get("/admin/admins")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertIn("http://localhost/admin/login" ,resp.location)

            login_as_admin(self, client)

            resp = client.get("/admin/admins")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Active Accounts', html)
            self.assertIn('Inactive Accounts', html)


    def test_admins_new(self):
        """Testing the admins_new"""

        with app.test_client() as client:
            resp = client.get("/admin/admins/new")

            self.assertEqual(resp.status_code , 302)
            self.assertIn("http://localhost/admin/login" , resp.location)


            login_as_admin(self , client)

            resp = client.get("/admin/admins/new")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('New Account', html)

            # post duplicate username / email

            admin = Admin.query.get(self.admin_username)

            post_data= {
                "username": self.admin_username,
                "password": "test",
                "email": admin.email,
                "first_name":"f_test",
                "last_name":"l_test",
                "authorization": "regular"
            }

            resp = client.post("/admin/admins/new", data=post_data)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Username taken', html)
            self.assertIn('Email taken', html)

            # post username / email

            post_data["username"] = "testuser"
            post_data["email"] = "test@ybdevs.com"
            resp = client.post("/admin/admins/new", data=post_data, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Successfully Created New Account!', html)

    
    def test_admins_update(self):
        """Testing the admins_update"""

        with app.test_client() as client:

            new_admin = Admin.register(username="test" , password="1234" , email="test@test.com" , first_name="f" , last_name="l")

            db.session.add(new_admin)
            db.session.commit()


            resp = client.get(f"/admin/admins/{new_admin.username}/update")

            self.assertEqual(resp.status_code , 302)
            self.assertIn("http://localhost/admin/login" , resp.location)


            login_as_admin(self , client)

            resp = client.get(f"/admin/admins/{new_admin.username}/update")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edit Account', html)
            self.assertIn(new_admin.username , html)

            # post duplicate email

            admin = Admin.query.get(self.admin_username)

            post_data= {
                "username": new_admin.username,
                "password": "test",
                "email": admin.email,
                "first_name":"f_test",
                "last_name":"l_test",
                "authorization": "regular"
            }

            resp = client.post(f"/admin/admins/{new_admin.username}/update", data=post_data)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Email taken', html)

            # post username / email

            post_data["email"] = "test@ybdevs.com"
            resp = client.post(f"/admin/admins/{new_admin.username}/update", data=post_data, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Successfully Update Account!', html)

    def test_password_reset(self):
        """Testing the password_reset"""

        with app.test_client() as client:
            resp = client.get("/admin/admins/password_reset")

            html = resp.get_data(as_text=True)

            admin = Admin.query.get(self.admin_username)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Admin Password Reset', html)
            self.assertIn('Email', html)
            self.assertIn('Input your email with your account here', html)

            # email exists
            resp = client.post("/admin/admins/password_reset", data={
                "email": admin.email
            }, follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("The reset email has been sent to you email address!" , html)

            # email not exist
            resp = client.post("/admin/admins/password_reset", data={
                "email": 'test@tes.com'
            }, follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Email is not found!" , html)

            admin = Admin.query.get(self.admin_username)

            # invalid token
            resp = client.get(f"/admin/admins/password_reset?token={admin.pwd_token}1" , follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Invalid Token, please try again!" , html)

            # right token
            resp = client.get(f"/admin/admins/password_reset?token={admin.pwd_token}")

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("New Password" , html)

            # update new password
            resp = client.post(f"/admin/admins/password_reset?token={admin.pwd_token}", data={
                "password": "test2"
            }, follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Successfully reset password!" , html)


            admin = admin.query.get(self.admin_username)
            self.assertEqual(admin.pwd_token , '')
            self.assertEqual(check_password_hash(admin.password , "test2") , True)

    def test_password_update(self):
        """Testing the password_update"""

        with app.test_client() as client:

            resp = client.get("/admin/admins/password")

            self.assertEqual(resp.status_code , 302)
            self.assertIn("http://localhost/admin/login" , resp.location)


            login_as_admin(self , client)

            resp = client.get("/admin/admins/password")

            html = resp.get_data(as_text=True)

            admin = Admin.query.get(self.admin_username)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edit Password', html)

            resp = client.post("/admin/admins/password", data={
                "password": "test" ,
                "password_confirm": "test1"
            }, follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Password must match" , html)


            resp = client.post("/admin/admins/password", data={
                "password": "test" ,
                "password_confirm": "test"
            }, follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Successfully Updated Password!" , html)

    def test_admins_delete(self):
        """Testing the admins_delete"""

        with app.test_client() as client:

            resp = client.post(f"/admin/admins/{self.admin_username}/delete")

            self.assertEqual(resp.status_code , 302)
            self.assertIn("http://localhost/admin/login" , resp.location)


            login_as_admin(self , client)

            # can't delete own account
            resp = client.post(f"/admin/admins/{self.admin_username}/delete", follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Unable to delete your own account!" , html)

            new_admin = Admin.register(username="test" , password="1234" , email="test@test.com" , first_name="f" , last_name="l")

            db.session.add(new_admin)
            db.session.commit()

            resp = client.post(f"/admin/admins/{new_admin.username}/delete", follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Successfull deactivate an account!" , html)