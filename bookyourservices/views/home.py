from flask import Blueprint, render_template , g , request
from google_calendar.google_calendar import *
from models import *

home = Blueprint('home', __name__)

@home.route('/')
def index():
    # Do some stuff

    services = Service.query.filter(Service.is_active==True).order_by(Service.updated.desc()).all()

    return render_template("home/index.html" , services=services)