
"""Default Configurations"""
import os
import json


def read_config_from_secret(key):
    """Read the config information from secret.py"""
    try:
        with open("secret.py", "r") as f:
            str = f.read()

            config = json.loads(str)

            return config.get(key, "")
    except:
        return ""


# database setting
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL', 'postgres:///bookyourservices')
SQLALCHEMY_TRACK_MODIFICATIONS = bool(os.environ.get(
    'SQLALCHEMY_TRACK_MODIFICATIONS', 'False'))
SQLALCHEMY_ECHO = bool(os.environ.get('SQLALCHEMY_ECHO', 'True'))

# security key
SECRET_KEY = os.environ.get('SECRET_KEY', b'Iq\x18N\xefk\x1c|\x9bx\xe8\xf5\x95\xf5 \xb4')


# url
BASE_URL = os.environ.get('BASE_URL', 'http://127.0.0.1:5000')

# debug setting
DEBUG_TB_INTERCEPT_REDIRECTS = bool(os.environ.get('DEBUG_TB_INTERCEPT_REDIRECTS' ,False))
DEBUG = bool(os.environ.get('DEBUG', True))
DEVELOPMENT = bool(os.environ.get('DEVELOPMENT', True))

# google account setting
GOOGLE_SERVICE_ACCOUNT_KEY = "SERVICE_ACCOUNT"
GOOGLE_SERVICE_ACCOUNT_FILE = 'google_calendar/service.json'

# time zone
DEFAULT_TIMEZONE = 'America/New_York'

# DateTime Format
DATETIME_FORMAT = '%a, %d. %b %Y %I:%M%p'
DATE_FORMAT = '%a, %d. %b %Y'

WEEKDAYS = ["SUNDAY", "MONDAY", "TUESDAY",
            "WEDNESDAY", "THURDAY", "FRIDAY", "SATURDAY"]

# encoding
DEFAULT_ENCODING = 'utf-8'

# session setting
USERNAME_SESSION_KEY = 'username'

ADMIN_USER_SESSION_KEY = 'admin_username'

ADMIN_AUTH_VALUE = 'administrator'

# upload setting
UPLOAD_TO_AWS_S3 = bool(os.environ.get("UPLOAD_TO_AWS_S3" , False))
AWS_S3_BUCKET = os.environ.get("AWS_S3_BUCKET" , "bookyourservices")

STATIC_FOLDER = os.path.join(os.path.dirname(__file__), "static/")
UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, "upload/")
UPLOAD_FOLDER_URL = "/static/upload/"
IMAGE_ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024

# default image url
DEFAULT_IMAGE_USER = "/static/images/default-user.png"
DEFAULT_IMAGE_SERVICE = "/static/images/default-service.jpg"

USER_UPLOAD_DIRNAME = 'users'
SERVICE_UPLOAD_DIRNAME = 'services'

# flash message
FLASH_GROUP_DANGER = "danger"
FLASH_GROUP_SUCCESS = "success"

# paginate
ADMIN_USERS_PER_PAGE = 20

# US States data
# United States of America Python Dictionary to translate States,
# Districts & Territories to Two-Letter codes and vice versa.
#
# https://gist.github.com/rogerallen/1583593
#
# Dedicated to the public domain.  To the extent possible under law,
# Roger Allen has waived all copyright and related or neighboring
# rights to this code.
US_STATE_ABBREV = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands': 'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

# US
US_ABBREV_STATES = dict(map(reversed, US_STATE_ABBREV.items()))


# mail setting
MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
MAIL_USE_SSL = bool(os.environ.get('MAIL_USE_SSL', 'True'))
MAIL_USERNAME = os.environ.get(
    'MAIL_USERNAME', read_config_from_secret('MAIL_USERNAME'))
MAIL_PASSWORD = os.environ.get(
    'MAIL_PASSWORD', read_config_from_secret('MAIL_PASSWORD'))

MAIL_SENDER = os.environ.get('MAIL_SENDER', 'ybdevs.com@gmail.com')
