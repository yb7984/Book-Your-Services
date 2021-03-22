"""Seed file to make sample data for db."""

from models import *
from app import *
from utils import *
import requests
import random

# Create all tables
db.drop_all()
db.create_all()

a = Admin(
    username='admin' ,
    first_name='admin' ,
    last_name='admin' ,
    email='bobowu@outlook.com',
    password=hash_password('1234') ,
    authorization='administrator' ,
    is_active=True
)

db.session.add(a)
db.session.commit()


a = Admin(
    username='admin_test' ,
    first_name='admin_test' ,
    last_name='admin_test' ,
    email='ybdevs.com@gmail.com',
    password=hash_password('1234') ,
    authorization='regular' ,
    is_active=True
)

db.session.add(a)
db.session.commit()

categories = [
    Category(name="Finance") ,
    Category(name="Accounting") ,
    Category(name="Taxes"),
    Category(name="Investment") ,
    Category(name="Auto Insurance") ,
    Category(name="Home Insurance") ,
    Category(name="Life Insurance")
]
db.session.add_all(categories)
db.session.commit()

resp = requests.get('https://randomuser.me/api/?results=50')

data = resp.json()

users = [
    User(username=item["login"]["username"] ,
    first_name=item["name"]["first"],
    last_name=item["name"]["last"],
    email=item["email"],
    password=hash_password("1234"),
    phone="8868878888" ,
    description="",
    is_provider=False) for item in data["results"]
    ]
for user in users:
    db.session.add(user)
    db.session.commit()


resp = requests.get('https://randomuser.me/api/?results=30')

data = resp.json()

users = [
    User(username=item["login"]["username"] ,
    first_name=item["name"]["first"],
    last_name=item["name"]["last"],
    email=item["email"],
    password=hash_password("1234"),
    phone="8868878888" ,
    description="",
    is_provider=True) for item in data["results"]
    ]

for user in users:
    db.session.add(user)
    db.session.commit()


for i in range(50):
    user_index  = random.randrange(0 , 20)
    user = User.query.get(users[user_index].username)
    category = Category.query.get(random.randrange(1 , 8))
    service = Service(username=user.username , name=f"{user.last_name}'s {category.name} Service" , description=f"Professional {category.name} Service from {user.full_name}")
    db.session.add(service)
    db.session.commit()

    service.set_categoiry_ids(ids=[category.id])
    db.session.commit()



#schedule
for user in users:
    schedule = Schedule(
        username=user.username , 
        date_exp=str(random.randrange(2)) ,
        schedules='[{"start": "09:00", "end": "10:00"} , {"start": "11:00", "end": "12:00"}]')

    db.session.add(schedule)
    db.session.commit()


    schedule = Schedule(
        username=user.username , 
        date_exp=str(random.randrange(2,4)) ,
        schedules='[{"start": "13:00", "end": "14:00"} , {"start": "14:00", "end": "15:00"}]')

    db.session.add(schedule)
    db.session.commit()

    schedule = Schedule(
        username=user.username , 
        date_exp=str(random.randrange(4 , 7)) ,
        schedules='[{"start": "10:00", "end": "12:00"} , {"start": "15:00", "end": "16:00"}]')

    db.session.add(schedule)
    db.session.commit()

