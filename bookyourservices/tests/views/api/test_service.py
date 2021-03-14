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

class APIServiceTest(TestCase):
    """Test class for Service API"""

    def setUp(self):
        """Clean up test data and set up some new data"""
        set_test_data(self)

        set_data_services(count=30 , provider_username=self.provider_username)

    def tearDown(self):
        """Clean up any faulted transaction."""
        db.session.rollback()

    def test_services_list(self):
        """Testing the services_list"""

        with app.test_client() as client:
            resp = client.get("/api/services")

            data = resp.get_json()
            
            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data["total"] , 31)
            self.assertEqual(data["page"] , 1)
            self.assertEqual(data["per_page"] , 12)
            self.assertEqual(data["pages"] , 3)
            self.assertEqual(len(data["items"]) , 12)


            resp = client.get("/api/services?page=3")

            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data["total"] , 31)
            self.assertEqual(data["page"] , 3)
            self.assertEqual(data["per_page"] , 12)
            self.assertEqual(data["pages"] , 3)
            self.assertEqual(len(data["items"]) , 7)

            resp = client.get(f"/api/services?username={self.provider_username}")

            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data["total"] , 31)
            self.assertEqual(data["page"] , 1)
            self.assertEqual(data["per_page"] , 12)
            self.assertEqual(data["pages"] , 3)
            self.assertEqual(len(data["items"]) , 12)


            resp = client.get(f"/api/services?username=test")

            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data["total"] , 0)
            self.assertEqual(data["page"] , 1)
            self.assertEqual(data["per_page"] , 12)
            self.assertEqual(data["pages"] , 0)
            self.assertEqual(len(data["items"]) , 0)

            resp = client.get(f"/api/services?categories={self.category_id}")

            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data["total"] , 1)
            self.assertEqual(data["page"] , 1)
            self.assertEqual(data["per_page"] , 12)
            self.assertEqual(data["pages"] , 1)
            self.assertEqual(len(data["items"]) , 1)

            resp = client.get(f"/api/services?term=service_")

            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data["total"] , 30)
            self.assertEqual(data["page"] , 1)
            self.assertEqual(data["per_page"] , 12)
            self.assertEqual(data["pages"] , 3)
            self.assertEqual(len(data["items"]) , 12)

    def test_services_list_mine(self):
        """Testing the services_list_mine"""

        with app.test_client() as client:
            resp = client.get("/api/services/mine")

            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data["error"] , "Unauthorized visit!")


            login_as_customer(self , client)

            resp = client.get("/api/services/mine")

            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data , {})

            login_as_provider(self , client)

            resp = client.get("/api/services/mine")

            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data["total"] , 31)
            self.assertEqual(data["page"] , 1)
            self.assertEqual(data["per_page"] , 12)
            self.assertEqual(data["pages"] , 3)
            self.assertEqual(len(data["items"]) , 12)


    def test_services_insert(self):
        """Testing the services_insert"""

        with app.test_client() as client:
            # not login 
            resp = client.post("/api/services" , data={
                "service-username": self.provider_username ,
                "service-name" : "test_service_test" ,
                "service-description" : "description" ,
                "service-is_active" : "y" ,
                "service-category_ids" : f"{self.category_id}"
            })

            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data["error"] , "Unauthorized visit!")


            # customer can't insert service
            login_as_customer(self , client)

            resp = client.post("/api/services" , data={
                "service-username": self.provider_username ,
                "service-name" : "test_service_test" ,
                "service-description" : "description" ,
                "service-is_active" : "y" ,
                "service-category_ids" : f"{self.category_id}"
            })

            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data , {"error" : "Unauthorized visit!"})

            # provider
            login_as_provider(self , client)

            resp = client.post("/api/services" , data={
                "service-username": self.provider_username ,
                "service-name" : "test_service_test" ,
                "service-description" : "description" ,
                "service-is_active" : "y" ,
                "service-category_ids" : f"{self.category_id}"
            })

            data = resp.get_json()

            self.assertEqual(resp.status_code , 201)
            self.assertGreater(data["item"]["id"] , 0)
            self.assertEqual(data["item"]["name"] , "test_service_test")
            self.assertEqual(data["item"]["category_ids"] , [self.category_id])

            # name no value, return errors
            resp = client.post("/api/services" , data={
                "service-username": "" ,
                "service-name" : "" ,
                "service-description" : "description" ,
                "service-is_active" : "y" ,
                "service-category_ids" : f"{self.category_id}"
            })

            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data["errors"] , {"name" : ["This field is required."]})

    def test_services_update(self):
        """Testing the services_update"""

        with app.test_client() as client:
            # not login 
            resp = client.patch(f"/api/services/{self.service_id}" , data={
                "service-username": self.provider_username ,
                "service-name" : "test_service_test" ,
                "service-description" : "description" ,
                "service-is_active" : "y" ,
                "service-category_ids" : f"{self.category_id}"
            })

            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data["error"] , "Unauthorized visit!")


            # not the service owner can't update the service 
            login_as_customer(self , client)

            resp = client.patch(f"/api/services/{self.service_id}" , data={
                "service-username": self.provider_username ,
                "service-name" : "test_service_test" ,
                "service-description" : "description" ,
                "service-is_active" : "y" ,
                "service-category_ids" : f"{self.category_id}"
            })

            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data , {"error" : "Unauthorized visit!"})

            # provider
            login_as_provider(self , client)

            resp = client.patch(f"/api/services/{self.service_id}" , data={
                "service-username": self.provider_username ,
                "service-name" : "test_service_test" ,
                "service-description" : "description" ,
                "service-is_active" : "y" ,
                "service-category_ids" : f"{self.category_id}"
            })

            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data["item"]["id"] , self.service_id)
            self.assertEqual(data["item"]["name"] , "test_service_test")
            self.assertEqual(data["item"]["category_ids"] , [self.category_id])

            # name no value, return errors
            resp = client.patch(f"/api/services/{self.service_id}" , data={
                "service-username": "" ,
                "service-name" : "" ,
                "service-description" : "description" ,
                "service-is_active" : "y" ,
                "service-category_ids" : f"{self.category_id}"
            })

            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data["errors"] , {"name" : ["This field is required."]})

    def test_services_delete(self):
        """Testing the services_delete"""

        with app.test_client() as client:
            # not login 
            resp = client.delete(f"/api/services/{self.service_id}")

            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data["error"] , "Unauthorized visit!")


            # customer can't insert service
            login_as_customer(self , client)

            resp = client.delete(f"/api/services/{self.service_id}")

            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data , {})

            service = Service.query.get(self.service_id)

            self.assertEqual(service.is_active , True)

            # provider
            login_as_provider(self , client)

            resp = client.delete(f"/api/services/{self.service_id}")
            data = resp.get_json()

            self.assertEqual(resp.status_code , 200)
            self.assertEqual(data , {})

            service = Service.query.get(self.service_id)

            self.assertEqual(service.is_active , False)