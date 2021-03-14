from flask import Blueprint, render_template, g, request, flash, url_for, jsonify
from secrets import token_urlsafe
from utils import *
from forms import *
from models import *
from views.modules.user import UserHandler
from views.modules.service import ServiceHandler
from views.modules.category import CategoryHandler
from views.modules.appointment import AppointmentHandler
from views.modules.schedule import ScheduleHandler


api = Blueprint('api', __name__)


############
# filters for displaying on templates


@api.app_template_filter('dt')
def _jinja2_filter_datetime(dt):

    return dt.strftime(DATETIME_FORMAT)


@api.app_template_filter('d')
def _jinja2_filter_date(d):

    return dt.strftime(DATE_FORMAT)

def unauthorized_visit():
    """Return the unauthorized visit error message"""

    return jsonify(error="Unauthorized visit!")


###########
# User Login methods


def login_required(func):
    """
    For the route need to login
    Check if the username in session
    Redirect to login page if not login yet
    """

    @wraps(func)
    def func_wrapper(*args, **kwargs):
        if login_username() is None and login_admin_username() is None:
            return unauthorized_visit()

        return func(*args, **kwargs)

    return func_wrapper


###########
# Admin login methods


def login_admin_required(func):
    """
    For the route need to login as admin
    Check if the username in session
    Redirect to login page if not login yet
    """

    @wraps(func)
    def func_wrapper(*args, **kwargs):
        if login_admin_username() is None:
            return unauthorized_visit()

        return func(*args, **kwargs)

    return func_wrapper


@api.before_request
def before_request_func():
    """Set current login user information"""

    g.global_values = {}

    if login_username():
        g.user = User.query.get(login_username())

        if g.user is not None:
            g.global_values["CURRENT_USERNAME"] = g.user.username

        if g.user is None:
            session.clear()

    if login_admin_username():
        g.admin = Admin.query.get(login_admin_username())

        if g.admin is not None:
            g.global_values["CURRENT_ADMIN_USERNAME"] = g.admin.username

        if g.admin is None:
            session.clear()


@api.route('/api/categories')
def categories_list():
    """Show all the categories"""

    items = CategoryHandler.list(only_active=(False if login_admin_username() is not None else True))

    return jsonify(items=[item.serialize() for item in items])


@api.route('/api/categories', methods=['POST'])
@login_admin_required
def categories_insert():
    """New Category"""

    item = CategoryHandler.insert()

    if "item" in item:
        return (jsonify(item) , 201)

    return (jsonify(item) , 200)


@api.route('/api/categories/<int:category_id>', methods=['PATCH'])
@login_admin_required
def categories_update(category_id):
    """Edit Category"""

    item = CategoryHandler.update(category_id)

    return (jsonify(item) , 200)


@api.route('/api/categories/<int:category_id>', methods=['DELETE'])
@login_admin_required
def categories_delete(category_id):
    """Delete category"""

    return (jsonify(CategoryHandler.delete(category_id)) , 200)


######
# For Services
#
@api.route('/api/services')
def services_list():
    """List for services"""

    pagenate = ServiceHandler.list(only_active=True)

    return jsonify_paginate(pagenate)

@api.route('/api/services/mine')
@login_required
def services_list_mine():
    """List for services for current user"""

    username = login_username()
    if login_admin_username() is not None:
        username = request.args.get("username" , "")

    user = User.query.get(username)

    if not user.is_provider:
        return jsonify({})

    pagenate = ServiceHandler.list(username=username , only_active=False)

    return jsonify_paginate(pagenate)


@api.route('/api/services' , methods=['POST'])
@login_required
def services_insert():
    """insert for services"""

    username = login_username()
    if login_admin_username() is not None:
        username = request.args.get("username" , "")

    user = User.query.get(username)

    if not user.is_provider:
        return unauthorized_visit()

    item = ServiceHandler.insert(username)

    if "item" in item:
        return (jsonify(item) , 201)

    return (jsonify(item) , 200)

@api.route('/api/services/<int:service_id>', methods=['PATCH'])
@login_required
def services_update(service_id):
    """Update Service"""
    service = Service.query.get(service_id)

    username = login_username()
    if login_admin_username() is not None:
        username = request.args.get("username" , "")

    if service is not None and service.username == username:
        item = ServiceHandler.update(service_id)
        return (jsonify(item) , 200)
    else:
        return jsonify({"error" : "Unauthorized visit!"})

@api.route('/api/services/<int:service_id>', methods=['DELETE'])
@login_required
def services_delete(service_id):
    """Delete Service"""
    service = Service.query.get(service_id)

    username = login_username()
    if login_admin_username() is not None:
        username = request.args.get("username" , "")

    if service is not None and service.username == username:
        return (jsonify(ServiceHandler.delete(service_id)) , 200)

    return (jsonify({}) , 200)



######
# For Schedules
#
@api.route('/api/schedules/<string:username>/<string:schedule_type>')
def schedules_list(username, schedule_type):
    """List for schedules"""

    items = ScheduleHandler.list(username=username , schedule_type=schedule_type)

    return jsonify(items = [item.serialize() for item in items])

@api.route('/api/schedules/<string:username>/<string:date>/<int:appointment_id>')
def schedules_list_available_times(username , date , appointment_id):
    """Return available schedules for the date"""

    list = ScheduleHandler.get_available_times(username , datetime.date.fromisoformat(date) , appointment_id=appointment_id)
    
    return jsonify(items=list)

@api.route('/api/schedules/<string:username>', methods=['POST'])
@login_required
def schedules_update(username):
    """update /insert for schedules"""

    user = User.query.get(username)

    if not user.is_provider:
        return unauthorized_visit()

    if login_username() == username or login_admin_username() is not None:
        item = ScheduleHandler.update(username)

        return (jsonify(item) , 200)

    return unauthorized_visit()


@api.route('/api/schedules/<string:username>/<string:date_exp>', methods=['DELETE'])
@login_required
def schedules_delete(username , date_exp):
    """Delete Schedule"""
    if login_username() == username or login_admin_username() is not None:
        return (jsonify(ScheduleHandler.delete(username , date_exp)) , 200)

    return unauthorized_visit()


######
# For Providers
#
@api.route('/api/providers')
def providers_list():
    """List for providers"""

    pagenate = UserHandler.list(only_active=True , provider_only=True)

    return jsonify_paginate(pagenate)


######
# For Appointment
#

@api.route('/api/appointments/<string:username>')
@login_required
def appointments_list(username):
    """insert for appointment"""

    if (login_username() == username or login_admin_username() is not None):

        per_page = request.args.get("per_page" , "12")
        
        paginate = AppointmentHandler.list(username , int(per_page))

        return jsonify_paginate(paginate)

    return jsonify({})

@api.route('/api/appointments' , methods=['POST'])
@login_required
def appointments_insert():
    """insert for appointment"""

    item = AppointmentHandler.insert(login_username())

    if "item" in item:
        return (jsonify(item) , 201)

    return (jsonify(item) , 200)


@api.route('/api/appointments/<int:appointment_id>' , methods=['PATCH'])
@login_required
def appointments_update(appointment_id):
    """update for appointment"""

    item = AppointmentHandler.update(login_username() , appointment_id)

    return (jsonify(item) , 200)


@api.route('/api/appointments/<int:appointment_id>' , methods=['DELETE'])
@login_required
def appointments_delete(appointment_id):
    """update for appointment"""

    item = AppointmentHandler.delete(login_username() , appointment_id)

    return (jsonify(item) , 200)

