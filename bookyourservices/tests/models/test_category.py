from unittest import TestCase
from app import app
from utils import *
from models import *
from secrets import token_urlsafe

from tests.test_common import test_setup

test_setup(app=app , db=db)


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
