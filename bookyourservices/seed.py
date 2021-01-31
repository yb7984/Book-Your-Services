"""Seed file to make sample data for db."""

from models import *
from app import *
from utils import *

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

