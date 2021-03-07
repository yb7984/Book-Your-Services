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
from google_calendar.google_calendar import GoogleCalendarHandler


api = Blueprint('api', __name__)


############
# filters for displaying on templates


@api.app_template_filter('dt')
def _jinja2_filter_datetime(dt):

    return dt.strftime(DATETIME_FORMAT)


@api.app_template_filter('d')
def _jinja2_filter_date(d):

    return dt.strftime(DATE_FORMAT)


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
    pagenate = ServiceHandler.list(username=login_username() , only_active=False)

    return jsonify_paginate(pagenate)


@api.route('/api/services' , methods=['POST'])
@login_required
def services_insert():
    """insert for services"""

    item = ServiceHandler.insert(login_username())

    if "item" in item:
        return (jsonify(item) , 201)

    return (jsonify(item) , 200)

@api.route('/api/services/<int:service_id>', methods=['PATCH'])
@login_required
def services_update(service_id):
    """Update Service"""
    service = Service.query.get(service_id)

    if service is not None and service.username == login_username():
        item = ServiceHandler.update(service_id)
        return (jsonify(item) , 200)
    else:
        return {"error": "Error when updating an service"}

@api.route('/api/services/<int:service_id>', methods=['DELETE'])
@login_required
def services_delete(service_id):
    """Delete Service"""
    service = Service.query.get(service_id)

    if service is not None and service.username == login_username():
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

@api.route('/api/schedules/<string:username>/<string:date_exp>', methods=['GET'])
def schedules_get(username, date_exp):
    """Get Schedule"""
    item = ScheduleHandler.get(username , date_exp)

    return jsonify(item=item.serialize())

@api.route('/api/schedules/<string:username>', methods=['POST'])
@login_required
def schedules_update(username):
    """update /insert for schedules"""

    if login_username() == username:
        item = ScheduleHandler.update(username)

        return (jsonify(item) , 200)

    return (jsonify({}) , 200)


@api.route('/api/schedules/<string:username>/<string:date_exp>', methods=['DELETE'])
@login_required
def schedules_delete(username , date_exp):
    """Delete Schedule"""
    if login_username() == username:
        return (jsonify(ScheduleHandler.delete(username , date_exp)) , 200)

    return jsonify({} , 200)


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
@api.route('/api/appointments' , methods=['POST'])
@login_required
def appointments_insert():
    """insert for appointment"""

    item = AppointmentHandler.insert(login_username())

    if "item" in item:
        return (jsonify(item) , 201)

    return (jsonify(item) , 200)


@api.route('/api/appointments')
@login_required
def appointments_list():
    """insert for appointment"""

    paginate = AppointmentHandler.list(login_username())

    return jsonify_paginate(paginate)
