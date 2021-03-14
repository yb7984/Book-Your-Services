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


class AppointmentModelTest(TestCase):
    """Test class for Data Model"""

    def setUp(self):
        """Clean up any exists appointment and insert a test appointment"""
        User.query.delete()
        Appointment.query.delete()

        customer = User.register(username="customer", email="test@test.com",
                             first_name="fcustomer", last_name="lcustomer", password='test')
        provider = User.register(username="provider", email="test@test.com",
                             first_name="fprovider", last_name="lprovider", password='test' , is_provider=True)
        db.session.add(customer)
        db.session.add(provider)

        service = Service(username="provider" , name="test service")
        db.session.add(service)
        db.session.commit()

        self.customer = customer
        self.provider = provider
        self.service = service

        appointment = Appointment(
            provider_username=provider.username,
            customer_username=customer.username,
            service_id=service.id,
            start= datetime.datetime.fromisoformat('2021-03-20 07:00:00'),
            end= datetime.datetime.fromisoformat('2021-03-20 08:00:00'),
            note="test note"
        )
        db.session.add(appointment)
        db.session.commit()

        self.appointment = appointment

    def tearDown(self):
        """Clean up any faulted transaction."""
        db.session.rollback()

        Appointment.query.filter(Appointment.id==self.appointment.id).delete()
        Service.query.filter(Service.id==self.service.id).delete()
        User.query.filter(User.username == self.provider.username).delete()
        User.query.filter(User.username == self.customer.username).delete()

        db.session.commit()

    def test_summary(self):
        """Testing the summary property"""
        item = self.appointment

        self.assertEqual(item.summary , f"{self.service.name} with {self.customer.full_name}")

    def test_description(self):
        """Testing the description property"""
        item = self.appointment

        self.assertEqual(item.description , f"""Service:{self.service.name}
Customer:{self.customer.full_name}
Provider:{self.provider.full_name}
Time:{item.start} to {item.end}
Note:{item.note}""")


    def test_check_available(self):
        """Testing the check_available method"""

        self.assertEqual(Appointment.check_available(username=self.provider.username , 
            start= datetime.datetime.fromisoformat('2021-03-20 07:59:00'),
            end= datetime.datetime.fromisoformat('2021-03-20 09:00:00'),
            appointment_id=0) , False)

        self.assertEqual(Appointment.check_available(username=self.provider.username , 
            start= datetime.datetime.fromisoformat('2021-03-20 06:00:00'),
            end= datetime.datetime.fromisoformat('2021-03-20 07:01:00'),
            appointment_id=0) , False)

        self.assertEqual(Appointment.check_available(username=self.provider.username , 
            start= datetime.datetime.fromisoformat('2021-03-20 07:00:00'),
            end= datetime.datetime.fromisoformat('2021-03-20 08:00:00'),
            appointment_id=0) , False)

        self.assertEqual(Appointment.check_available(username=self.provider.username , 
            start= datetime.datetime.fromisoformat('2021-03-20 08:00:00'),
            end= datetime.datetime.fromisoformat('2021-03-20 09:00:00'),
            appointment_id=0) , True)

        self.assertEqual(Appointment.check_available(username=self.provider.username , 
            start= datetime.datetime.fromisoformat('2021-03-20 06:00:00'),
            end= datetime.datetime.fromisoformat('2021-03-20 07:00:00'),
            appointment_id=0) , True)

    def test_available(self):
        """Testing the available method"""
        item = self.appointment

        new_appointment = Appointment(
            provider_username=self.provider.username,
            customer_username=self.customer.username,
            service_id=self.service.id,
            start= datetime.datetime.fromisoformat('2021-03-20 07:00:00'),
            end= datetime.datetime.fromisoformat('2021-03-20 08:00:00'),
            note="test note"
        )

        self.assertEqual(new_appointment.available , False)

        new_appointment.start = datetime.datetime.fromisoformat('2021-03-20 06:00')
        new_appointment.end = datetime.datetime.fromisoformat('2021-03-20 07:01')

        self.assertEqual(new_appointment.available , False)

        new_appointment.start = datetime.datetime.fromisoformat('2021-03-20 07:59')
        new_appointment.end = datetime.datetime.fromisoformat('2021-03-20 09:00')

        self.assertEqual(new_appointment.available , False)

        new_appointment.start = datetime.datetime.fromisoformat('2021-03-20 06:00')
        new_appointment.end = datetime.datetime.fromisoformat('2021-03-20 07:00')

        self.assertEqual(new_appointment.available , True)

        new_appointment.start = datetime.datetime.fromisoformat('2021-03-20 08:00')
        new_appointment.end = datetime.datetime.fromisoformat('2021-03-20 09:00')

        self.assertEqual(new_appointment.available , True)

    def test_repr(self):
        """Testing the __repr method"""
        item = self.appointment

        self.assertEqual(
            item.__repr__(), f"<Appointment id={item.id} provider_username={item.provider_username} customer_username={item.customer_username} start={item.start} end={item.end}>")

    def test_serialize(self):
        """Testing the serialize method"""

        item = self.appointment

        self.assertEqual(item.serialize(), {
            "id": item.id,
            "event_id": item.event_id,
            "provider_username": item.provider_username,
            "customer_username": item.customer_username,
            "start": item.start.isoformat(),
            "end": item.end.isoformat(),
            "service_id": item.service_id,
            "note": item.note,
            "summary": item.summary,
            "description": item.description,
            "updated": item.updated,
            "created": item.created,
            "is_active": item.is_active,
            "provider": item.provider.full_name,
            "customer": item.customer.full_name,
            "service": item.service.name
        })
