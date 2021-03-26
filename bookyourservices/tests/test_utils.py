from unittest import TestCase
from app import app
from utils import *
from models import *
from forms import *
from secrets import token_urlsafe
from wtforms.widgets import HiddenInput
from flask_sqlalchemy import Pagination
import config

# Use test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bookyourservices_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UtilsTest(TestCase):
    """Test class for Data Model"""

    def setUp(self):
        """Clean up any exists service and insert a test service"""
        User.query.delete()

        user = User.register(username="test", email="test@test.com",
                             first_name="fn", last_name="ln", password='test')
        db.session.add(user)
        db.session.commit()

        self.user = user

    def tearDown(self):
        """Clean up any faulted transaction."""
        db.session.rollback()

    def test_config_mail(self):
        """Testing the config_mail method"""

        config_mail(app)

        with app.app_context():
            with mail.record_messages() as outbox:

                mail.send_message(subject='testing',
                                  body='test',
                                  sender=config.MAIL_SENDER,
                                  recipients=['bobowu@outlook.com'])

                self.assertEqual(len(outbox),  1)
                self.assertEqual(outbox[0].subject, "testing")

    def test_hash_password(self):
        """Testing the hash_password method"""

        hash = hash_password("test")

        bcrypt.check_password_hash(hash, "test")

        self.assertEqual(bcrypt.check_password_hash(hash, "test"), True)
        self.assertEqual(bcrypt.check_password_hash(hash, "test1"), False)

    def test_check_password_hash(self):
        """Testing the check_password_hash method"""

        hash = hash_password("test")

        self.assertEqual(check_password_hash(hash, "test"), True)
        self.assertEqual(check_password_hash(hash, "test1"), False)

    def test_login_username(self):
        """Testing the login_username method"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session[USERNAME_SESSION_KEY] = "test"

            resp = client.get("/")

            self.assertEqual(login_username(), "test")

    def test_login_username_set(self):
        """Testing the login_username_set method"""

        with app.test_client() as client:
            resp = client.get("/")

            with app.app_context():
                login_username_set("test")

            self.assertEqual(login_username(), "test")

    def test_login_admin_username(self):
        """Testing the login_admin_username method"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session[ADMIN_USER_SESSION_KEY] = "admin"

            resp = client.get("/")

            self.assertEqual(login_admin_username(), "admin")

    def test_login_admin_username_set(self):
        """Testing the login_admin_username_set method"""

        with app.test_client() as client:
            resp = client.get("/")

            with app.app_context():
                login_admin_username_set("admin")

            self.assertEqual(login_admin_username(), "admin")

    def test_upload_allowed_file(self):
        """Testing the upload_allowed_file method"""

        self.assertEqual(upload_allowed_file('aaa.jpg'), True)
        self.assertEqual(upload_allowed_file('aaa.png'), True)
        self.assertEqual(upload_allowed_file('aaa.jpeg'), True)
        self.assertEqual(upload_allowed_file('aaa.gif'), True)
        self.assertEqual(upload_allowed_file('aaa.bmp'), False)
        self.assertEqual(upload_allowed_file('aaa.gif', {"bmp"}), False)
        self.assertEqual(upload_allowed_file('aaa.bmp', {"bmp"}), True)

    def test_replace_file_name(self):
        """Testing the replace_file_name method"""

        self.assertEqual(replace_file_name('aaa.jpg', ''), 'aaa.jpg')
        self.assertEqual(replace_file_name('aaa.jpg', 'bbb'), 'bbb.jpg')
        self.assertEqual(replace_file_name('aaa', 'bbb'), 'bbb')

    def test_make_dir(self):
        """Testing the make_dir method"""

        folder = os.path.join(UPLOAD_FOLDER, 'ttttt')
        self.assertEqual(os.path.isdir(folder), False)
        make_dir(folder)
        self.assertEqual(os.path.isdir(folder), True)

        os.rmdir(folder)

    def test_upload_file_url(self):
        """Testing the upload_file_url method"""

        self.assertEqual(upload_file_url('test'), '/static/upload/test')
        self.assertEqual(upload_file_url(
            'test', dirname='dir'), '/static/upload/dir/test')
        self.assertEqual(upload_file_url('test', username='user'),
                         '/static/upload/users/user/test')
        self.assertEqual(upload_file_url('test', username='user',
                                         dirname='dir'), '/static/upload/users/user/dir/test')

    def test_form_hide_value(self):
        """Testing the form_hide_value method"""
        with app.test_client() as client:
            resp = client.get("/")

            with app.app_context():
                form = UserForm()

                form_hide_value(form.password, '')

                self.assertIsInstance(form.password.widget, HiddenInput)

    def test_jsonify_paginate(self):
        """Testing the jsonify_paginate method"""

        with app.app_context():
            items = []

            for index in range(12):
                item = Category(name=str(index))

                items.append(item)

            page = Pagination(query=None, page=1, per_page=12,
                              total=30, items=items)

            resp = jsonify_paginate(page)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.is_json , True)

            data = resp.get_json()

            self.assertEqual(data["page"], 1)
            self.assertEqual(data["pages"], 3)
            self.assertEqual(data["per_page"], 12)
            self.assertEqual(data["total"], 30)
            self.assertEqual(len(data["items"]), 12)


    def test_localize_datetime(self):
        """Testing the localize_datetime method"""

        now = datetime.datetime.now()

        new_now = localize_datetime(now)

        self.assertEqual(now.tzinfo , None)
        self.assertEqual(str(new_now.tzinfo) , DEFAULT_TIMEZONE)