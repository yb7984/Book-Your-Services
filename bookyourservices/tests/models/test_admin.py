from unittest import TestCase
from app import app
from utils import *
from models import *
from secrets import token_urlsafe

#Use test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bookyourservices_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class AdminModelTest(TestCase):
    """Test class for Data Model"""

    def setUp(self):
        """Clean up any exists admins and insert a test account"""
        Admin.query.delete()

        item = Admin.register(username="test" , email="test@test.com" , first_name="fn" , last_name="ln", password='test')
        db.session.add(item)
        db.session.commit()

        self.admin = item

    def tearDown(self):
        """Clean up any faulted transaction."""
        db.session.rollback()

    def test_full_name(self):
        """Testing the full_name property"""
        item = Admin(username="ab" , first_name="A" , last_name="B")

        self.assertEqual(item.full_name , "A B")

    def test_repr(self):
        """Testing the __repr method"""
        item = Admin(username="ab" , first_name="A" , last_name="B" , email="a@b.com")

        self.assertEqual(item.__repr__() , f"<Admin {item.username} {item.first_name} {item.last_name} {item.email}>")

    def test_register(self):
        """Testing the register method"""
        item = Admin.register(username='username' , password='password' , email='a@b.com' , first_name='A' , last_name='B')

        self.assertEqual(item.username , 'username')
        self.assertEqual(check_password_hash(item.password , 'password'), True)
        self.assertEqual(item.email , 'a@b.com')
        self.assertEqual(item.first_name , 'A')
        self.assertEqual(item.last_name , 'B')


    def test_authenticate(self):
        """Testing the authenticate method"""
        item = Admin.authenticate(username='test' , password='test')

        self.assertIsNotNone(item)

        # wrong password
        item = Admin.authenticate(username='test' , password='test1')

        self.assertIsNotNone(item)

        # wrong username 
        item = Admin.authenticate(username='test1' , password='test1')

        self.assertIsNotNone(item)


    def test_update_password(self):
        """Testing the update_password method"""
        item = Admin.update_password(username='test' , password='test1')

        self.assertIsNotNone(item)
        self.assertIsNotNone(Admin.authenticate('test' , 'test1'))


        item = Admin.update_password(username='test1' , password='test1')
        self.assertEqual(item , False)

        Admin.update_password(username='test' , password='test')

    def test_update_password_by_token(self):
        """Testing the update_password_by_token method"""

        item = self.admin
        token = token_urlsafe()
        item.pwd_token = token
        db.session.commit()

        item = Admin.update_password_by_token(token=token , password='test1')

        self.assertIsNotNone(item)
        self.assertIsNotNone(Admin.authenticate('test' , 'test1'))


        item = Admin.update_password_by_token(token=token_urlsafe() , password='test1')
        self.assertEqual(item , False)

        Admin.update_password(username='test' , password='test')
