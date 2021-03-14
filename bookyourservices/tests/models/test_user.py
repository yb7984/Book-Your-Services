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


class UserModelTest(TestCase):
    """Test class for Data Model"""

    def setUp(self):
        """Clean up any exists users and insert a test account"""
        User.query.delete()

        item = User.register(username="test" , email="test@test.com" , first_name="fn" , last_name="ln", password='test')
        db.session.add(item)
        db.session.commit()

        self.user = item

    def tearDown(self):
        """Clean up any faulted transaction."""
        
        db.session.rollback()
        
        User.query.filter(User.username==self.user.username).delete()
        db.session.commit()

    def test_full_name(self):
        """Testing the full_name property"""
        item = User(username="ab" , first_name="A" , last_name="B")

        self.assertEqual(item.full_name , "A B")

    def test_image_url(self):
        """Testing the image_url property"""
        item = self.user

        self.assertEqual(item.image_url , DEFAULT_IMAGE_USER)

        item.image = 'test.jpg'
        self.assertEqual(item.image_url , upload_file_url('test.jpg' , username='test'))

    def test_repr(self):
        """Testing the __repr method"""
        item = User(username="ab" , first_name="A" , last_name="B" , email="a@b.com")

        self.assertEqual(item.__repr__() , f"<User {item.username} {item.first_name} {item.last_name} {item.email}>")

    def test_register(self):
        """Testing the register method"""
        item = User.register(username='username' , password='password' , email='a@b.com' , first_name='A' , last_name='B' , is_provider=False)

        self.assertEqual(item.username , 'username')
        self.assertEqual(check_password_hash(item.password , 'password'), True)
        self.assertEqual(item.email , 'a@b.com')
        self.assertEqual(item.first_name , 'A')
        self.assertEqual(item.last_name , 'B')
        self.assertEqual(item.is_provider, False)


    def test_authenticate(self):
        """Testing the authenticate method"""
        item = User.authenticate(username='test' , password='test')

        self.assertIsNotNone(item)

        # wrong password
        item = User.authenticate(username='test' , password='test1')

        self.assertIsNotNone(item)

        # wrong username 
        item = User.authenticate(username='test1' , password='test1')

        self.assertIsNotNone(item)


    def test_update_password(self):
        """Testing the update_password method"""
        item = User.update_password(username='test' , password='test1')

        self.assertIsNotNone(item)
        self.assertIsNotNone(User.authenticate('test' , 'test1'))


        item = User.update_password(username='test1' , password='test1')
        self.assertEqual(item , False)

        User.update_password(username='test' , password='test')

    def test_update_password_by_token(self):
        """Testing the update_password_by_token method"""

        item = self.user
        token = token_urlsafe()
        item.pwd_token = token
        db.session.commit()

        item = User.update_password_by_token(token=token , password='test1')

        self.assertIsNotNone(item)
        self.assertIsNotNone(User.authenticate('test' , 'test1'))


        item = User.update_password_by_token(token=token_urlsafe() , password='test1')
        self.assertEqual(item , False)

        User.update_password(username='test' , password='test')


    def test_serialize(self):
        """Testing the serialize method"""

        item = self.user

        self.assertEqual(item.serialize() , {
            "username": item.username,
            "full_name": item.full_name,
            "first_name": item.first_name,
            "last_name": item.last_name,
            "email": item.email,
            "phone": item.phone,
            "description": item.description,
            "image": item.image,
            "image_url": item.image_url,
            "is_provider": item.is_provider,
            "updated": item.updated,
            "created": item.created,
            "is_active": item.is_active
        })
