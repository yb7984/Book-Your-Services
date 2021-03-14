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

    def test_image_url(self):
        """Testing the image_url property"""
        item = self.service

        self.assertEqual(item.image_url , DEFAULT_IMAGE_SERVICE)

        item.image = 'test.jpg'
        self.assertEqual(item.image_url , upload_file_url('test.jpg', username=item.username, dirname="services"))

    def test_set_categoiry_ids(self):
        """Testing the set_categoiry_ids method"""
        
        service = Service.query.get(self.service.id)

        service.set_categoiry_ids([])

        db.session.commit()

        service = Service.query.get(self.service.id)

        self.assertEqual(service.categories , [])
        self.assertEqual(service.categories_services , [])

        service.set_categoiry_ids([self.category.id])
        db.session.commit()


        service = Service.query.get(self.service.id)

        self.assertEqual(len(service.categories) , 1)
        self.assertEqual(len(service.categories_services) , 1)

    def test_get_categoiry_ids(self):
        """Testing the get_category_ids method"""
        
        service = Service.query.get(self.service.id)

        self.assertEqual(service.get_category_ids() , [self.category.id])

    def test_repr(self):
        """Testing the __repr method"""
        item = self.service

        self.assertEqual(
            item.__repr__(), f"<Service name={item.name} username={item.username}>")

    def test_serialize(self):
        """Testing the serialize method"""

        item = self.service

        self.assertEqual(item.serialize(), {
            "id": item.id,
            "username": item.username,
            "name": item.name,
            "description": item.description,
            "image": item.image,
            "image_url": item.image_url,
            "updated": item.updated,
            "created": item.created,
            "is_active": item.is_active,
            "categories": [category.serialize() for category in item.categories],
            "category_ids": item.get_category_ids(),
            "provider": item.user.full_name
        })
