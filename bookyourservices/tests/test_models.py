from unittest import TestCase
from app import app
from utils import db, connect_db
from models import User,Post,Tag,PostTag, connect_db

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
        """Clean up any exists users."""
        User.query.delete()

    def tearDown(self):
        """Clean up any faulted transaction."""
        db.session.rollback()

    def test_full_name(self):
        """Testing the get_full_name method"""
        user = User(first_name="A" , last_name="B" , image_url="url")

        self.assertEqual(user.full_name , "A B")