from flask import Blueprint, render_template, g, request, flash, url_for, jsonify
from secrets import token_urlsafe
from utils import *
from forms import *
from models import *
from views.modules.user import UserHandler
from views.modules.address import AddressHandler
from views.modules.service import ServiceHandler
from views.modules.category import CategoryHandler
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


######
# For Providers
#
@api.route('/api/providers')
def providers_list():
    """List for providers"""

    pagenate = UserHandler.list(only_active=True , provider_only=True)

    return jsonify_paginate(pagenate)
