from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import request,session,flash,redirect
from config import *
import urllib.parse , os
from werkzeug.utils import secure_filename
from wtforms.widgets import HiddenInput
from flask_mail import Mail
import secret

db = SQLAlchemy()
bcrypt = Bcrypt()
 
mail = Mail()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

def config_mail(app):
    """Config flask mail"""

    app.config.update(
        MAIL_SERVER=MAIL_SERVER,
        MAIL_PORT=MAIL_PORT,
        MAIL_USE_SSL=MAIL_USE_SSL,
        MAIL_USERNAME = secret.MAIL_USERNAME,
        MAIL_PASSWORD = secret.MAIL_PASSWORD
    )

    mail = Mail(app)



def hash_password(pwd):
    """return the hashed password value"""

    hashed = bcrypt.generate_password_hash(pwd)
    # turn bytestring into normal string
    return hashed.decode(DEFAULT_ENCODING)

def check_password_hash(hashed_pwd , password):
    """Check if the hashed password matched the real password"""

    return bcrypt.check_password_hash(hashed_pwd, password)


def login_required(func):
    """
    For the route need to login
    Check if the username in session
    Redirect to login page if not login yet
    """

    @wraps(func)
    def func_wrapper(*args , **kwargs):
        if login_username() is None:
            flash("Please login first!", "danger")
            return redirect(f'/login?path={urllib.parse.quote_plus(request.path)}')

        return func(*args , **kwargs)

    return func_wrapper

def login_username():
    """Return current login username"""
    return session.get(USERNAME_SESSION_KEY , None)

def login_username_set(username):
    """Set current login username"""

    session[USERNAME_SESSION_KEY] = username


#upload methods
def upload_dir_user(username , subdir=""):
    """Return user's upload dir path"""
    if len(subdir) > 0:
        return f'{USER_UPLOAD_DIRNAME}/{username}/{subdir}'
    return f'{USER_UPLOAD_DIRNAME}/{username}'

def upload_allowed_file(filename , exts={}):
    """Check if file is allowed to upload"""
    if len(exts) == 0:
        exts = ALLOWED_EXTENSIONS

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def replace_file_name(filename , change_name=""):
    """Replace uploaded filename to a new filename with same extension"""

    change_name = str(change_name)
    if len(change_name.strip()) == 0:
        return filename

    if '.' in filename:
        return f"{change_name}.{filename.rsplit('.', 1)[1].lower()}"

    return change_name

def make_dir(folder):
    """Create the directory if not exists"""
    if not os.path.isdir(folder):
        os.makedirs(folder)

def upload_file(fieldname , name="" , dirname="" , exts={}):
    """Upload file and return the filename"""
    if len(request.files) == 0:
        return None

    file = request.files[fieldname]

    if file.filename != "" and file and upload_allowed_file(file.filename , exts):
        
        filename = replace_file_name(secure_filename(file.filename) , change_name=name)
        
        if len(dirname) > 0:
            folder = os.path.join(UPLOAD_FOLDER , dirname)
        else:
            folder = UPLOAD_FOLDER

        make_dir(folder)

        file_path = os.path.join(folder, filename)


        file.save(file_path)

        return filename
    return None


def upload_file_url(filename , username="" , dirname=""):
    """Return the url of an uploaded file"""

    if len(dirname) > 0:
        return f'{UPLOAD_FOLDER_URL}{USER_UPLOAD_DIRNAME}/{username}/{dirname}/{filename}'
    return f'{UPLOAD_FOLDER_URL}{USER_UPLOAD_DIRNAME}/{username}/{filename}'


def form_hide_value(field , value):
    """
    Hide the field by morping it into a 
    HiddenInput.    
    """ 
    field.widget = HiddenInput()
    # wtforms chokes if the data attribute is not present
    field.data = value
    # wtforms chokes on SelectField with HiddenInput widget
    # if there is no _data() callable
    field._value = lambda: value

