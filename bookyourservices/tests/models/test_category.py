from unittest import TestCase
from app import app
from utils import *
from models import *
from secrets import token_urlsafe

# Use test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bookyourservices_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class CategoryModelTest(TestCase):
    """Test class for Data Model"""

    def setUp(self):
        """Clean up categories and insert a test category"""
        Category.query.delete()

        item = Category(name="test")
        db.session.add(item)
        db.session.commit()

        self.category = item

    def tearDown(self):
        """Clean up any faulted transaction."""
        db.session.rollback()

        Category.query.filter(Category.id==self.category.id).delete()
        db.session.commit()

    def test_repr(self):
        """Testing the __repr method"""
        item = self.category

        self.assertEqual(
            item.__repr__(), f"<Category id={item.id} name={item.name}>")

    def test_serialize(self):
        """Testing the serialize method"""

        item = self.category

        self.assertEqual(item.serialize(), {
            "id": item.id,
            "name": item.name,
            "is_active": item.is_active
        })
