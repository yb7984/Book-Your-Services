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


class ServiceModelTest(TestCase):
    """Test class for Data Model"""

    def setUp(self):
        """Clean up any exists service and insert a test service"""
        User.query.delete()
        Category.query.delete()
        Service.query.delete()

        user = User.register(username="test" , email="test@test.com" , first_name="fn" , last_name="ln", password='test')
        db.session.add(user)
        db.session.commit()

        self.user = user

        category = Category(name="test category")
        db.session.add(category)
        db.session.commit()

        self.category = category

        service = Service(username=self.user.username , name="test service")
        db.session.add(service)
        db.session.commit()

        self.service = service

        service.categories.append(category)
        db.session.commit()

    def tearDown(self):
        """Clean up any faulted transaction."""
        db.session.rollback()

        Service.query.filter(Service.id==self.service.id).delete()
        db.session.commit()

        Category.query.filter(Category.id==self.category.id).delete()
        db.session.commit()

        User.query.filter(User.username==self.user.username).delete()
        db.session.commit()

    def test_repr(self):
        """Testing the __repr method"""
        item = self.service.categories_services[0]

        self.assertEqual(
            item.__repr__(), f"<CategoryService category_id={item.category_id} service_id={item.service_id}>")

    def test_serialize(self):
        """Testing the serialize method"""

        item = self.service.categories_services[0]

        self.assertEqual(item.serialize(), {
            "category_id": item.category_id,
            "service_id": item.service_id
        })
