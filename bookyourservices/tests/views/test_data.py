from datetime import date,timedelta,time
from utils import *
from config import *
from models import *


def set_test_data(test_class):
    """set the initial test data into the test database"""

    Appointment.query.delete()
    Service.query.delete()
    Category.query.delete()
    User.query.delete()
    Admin.query.delete()

    admin = Admin(
        username='admin' ,
        first_name='admin' ,
        last_name='admin' ,
        email='bobowu@outlook.com',
        password=hash_password('1234') ,
        authorization='administrator' ,
        is_active=True
    )

    db.session.add(admin)
    db.session.commit()

    test_class.admin_username = "admin"
    test_class.admin = admin

    # users
    customer = User.register(username="testcustomer", email="test_customer@test.com",
                             first_name="fcustomer", last_name="lcustomer", password='test')
    provider = User.register(username="testprovider", email="test_provider@test.com",
                             first_name="fprovider", last_name="lprovider", password='test', is_provider=True)
    db.session.add(customer)
    db.session.add(provider)

    test_class.customer = customer
    test_class.provider = provider

    test_class.customer_username = customer.username
    test_class.provider_username = provider.username

    # category
    category = Category(name="test category")
    db.session.add(category)
    db.session.commit()
    test_class.category_id = category.id
    test_class.category = category

    # service
    service = Service(username=provider.username, name="test service")
    db.session.add(service)
    db.session.commit()

    test_class.service_id = service.id
    test_class.service = service

    service.categories.append(category)
    db.session.commit()

    # schedule
    schedule = Schedule(username=provider.username, date_exp="1", schedules=json.dumps(
        [{"start": "07:00", "end": "08:00"}]
    ))
    db.session.add(schedule)
    db.session.commit()

    test_class.schedule_date_exp = schedule.date_exp
    test_class.schedule = schedule

    # make sure the date has schedules
    appointment_date = date.today() + timedelta(days=(1 if date.today().weekday() % 2 == 0 else 2))
    # appointment
    appointment = Appointment(
        provider_username=provider.username,
        customer_username=customer.username,
        service_id=service.id,
        start=datetime.datetime.combine(appointment_date, time(hour=10 , minute=30)),
        end=datetime.datetime.combine(appointment_date, time(hour=11 , minute=30)),
        note="test note"
    )

    # print(appointment)
    db.session.add(appointment)
    db.session.commit()

    test_class.appointment_id = appointment.id
    test_class.appointment = appointment

def set_data_customers(count):
    """Create customers"""
    for i in range(count):
        customer = User.register(username=f"testcustomer_{i}", email=f"test_customer_{i}@test.com",
                                first_name=f"fcustomer_{i}", last_name=f"lcustomer_{i}", password='test')

        db.session.add(customer)

    db.session.commit()


def set_data_providers(count):
    """Create providers"""
    for i in range(count):
        provider = User.register(username=f"testprovider_{i}", email=f"test_provider_{i}@test.com",
                             first_name=f"fprovider_{i}", last_name=f"lprovider_{i}", password='test', is_provider=True)
        db.session.add(provider)

    db.session.commit()

def set_data_categories(count):
    """Create categories"""
    for i in range(count):
        category = Category(name=f"category_{i}")
        db.session.add(category)
    db.session.commit()

def set_data_services(count , provider_username):
    """Create services"""
    for i in range(count):
        service = Service(username=provider_username, name=f"service_{provider_username}_{i}")
        db.session.add(service)
    db.session.commit()

def set_data_schedule(provider_username):
    """Create schedules"""

    for i in range(0 , 7 , 2):
        schedule = Schedule(username=provider_username , date_exp=str(i) , schedules=json.dumps(
            [{"start" : f"{h}:00", "end":f"{h+1}:00"} for h in range(10 , 16 , 2)]
        ))

        db.session.add(schedule)

    db.session.commit()

def set_data_appointment(provider_username , customer_username , service_id,  count):
    """Creat appointments"""


    for i in range(count):
        appointment_date = date.today() + timedelta(days=i)
        appointment = Appointment(
            provider_username=provider_username,
            customer_username=customer_username,
            service_id=service_id,
            start=datetime.datetime.combine(appointment_date, time(hour=7)),
            end=datetime.datetime.combine(appointment_date, time(hour=8)),
            note=f"test note {i}"
        )

        db.session.add(appointment)
    db.session.commit()


def login_as_customer(test_class , client):
    """login user as a customer"""

    with client.session_transaction() as change_session:
        change_session[USERNAME_SESSION_KEY] = test_class.customer_username

def login_as_provider(test_class, client):
    """login user as a provider"""

    with client.session_transaction() as change_session:
        change_session[USERNAME_SESSION_KEY] = test_class.provider_username


def login_as_admin(test_class, client):
    """login user as a provider"""

    with client.session_transaction() as change_session:
        change_session[ADMIN_USER_SESSION_KEY] = "admin"


