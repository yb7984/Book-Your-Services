
"""Default Configurations"""
import os

#database setting
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgres:///bookyourservices')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

#security key
SECRET_KEY = os.environ.get('SECRET_KEY', 'so so so')

#debug setting
DEBUG_TB_INTERCEPT_REDIRECTS = False
DEBUG = True
DEVELOPMENT = True

#google account setting
SERVICE_ACCOUNT_FILE = 'google_calendar/service.json'

#time zone
DEFAULT_TIMEZONE = 'America/New_York'

#DateTime Format
DATETIME_FORMAT = '%a, %d. %b %Y %I:%M%p'
DATE_FORMAT = '%a, %d. %b %Y'

#encoding
DEFAULT_ENCODING = 'utf-8'

#session setting
USERNAME_SESSION_KEY = 'username'

ADMIN_USER_SESSION_KEY = 'admin_username'

ADMIN_AUTH_VALUE='administrator'

#upload setting
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__) , "static/upload/")
UPLOAD_FOLDER_URL = "/static/upload/"
IMAGE_ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024

USER_UPLOAD_DIRNAME = 'users'

#paginate
ADMIN_USERS_PER_PAGE = 2