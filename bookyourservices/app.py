from flask import Flask , g
from views.home import home
from views.admin import admin
from flask_debugtoolbar import DebugToolbarExtension
import utils
import config
from datetime import date,datetime


app = Flask(__name__)

app.config.from_object('config')

# toolbar = DebugToolbarExtension(app)

utils.connect_db(app)


app.register_blueprint(home)
app.register_blueprint(admin)

