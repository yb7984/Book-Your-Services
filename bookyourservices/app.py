from flask import Flask , g
from views.home import home
from views.admin import admin
from flask_debugtoolbar import DebugToolbarExtension
import utils
import config
from datetime import date,datetime


app = Flask(__name__)

#load configs
app.config.from_object('config')

# toolbar = DebugToolbarExtension(app)

#connect to database
utils.connect_db(app)

#config flask mail
utils.config_mail(app)


app.register_blueprint(home)
app.register_blueprint(admin)

