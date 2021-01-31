from flask_wtf import FlaskForm
import re
from wtforms import StringField, BooleanField 
from wtforms.validators import InputRequired , Length


class CategoryForm(FlaskForm):
    """Form for insert / update categories"""
    name = StringField("Name", validators=[InputRequired(), Length(min=1 , max=100)], render_kw={"placeholder" : "Input the category name here"})
    is_active = BooleanField('Active')