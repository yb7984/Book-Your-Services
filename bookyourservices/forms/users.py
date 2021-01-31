from flask_wtf import FlaskForm
import re
from wtforms import StringField, PasswordField , TextAreaField , SelectField , BooleanField , FileField
from wtforms.fields.html5 import EmailField , IntegerField
from wtforms.validators import InputRequired, Email , Length , Optional , Regexp


class UserLoginForm(FlaskForm):
    """Form for admin login"""
    username = StringField("Username", validators=[InputRequired(), Length(min=3 , max=20)])
    password = PasswordField("Password", validators=[InputRequired()])

class UserForm(FlaskForm):
    """Form for insert user"""
    username = StringField("Username", validators=[InputRequired(), Length(min=3 , max=20)], render_kw={"placeholder" : "Input your username here, must be between 3 to 20 letters or numbers"})
    password = PasswordField("Password", validators=[InputRequired()] , render_kw={"placeholder": "Input your password here"})
    password_edit = PasswordField("Password", validators=[Optional()] , render_kw={"placeholder": "Input your password here"})
    first_name = StringField("First Name" , validators=[InputRequired() ,  Length(min=1 , max=30)], render_kw={"placeholder" : "Input your first name here"})
    last_name = StringField("Last Name" , validators=[InputRequired() , Length(min=1 , max=30)] , render_kw={"placeholder" : "Input your last name here"})
    email = EmailField("Email" , validators=[InputRequired() , Length(min=1 , max=50) , Email(message='Must be a valid email address')] , render_kw={"placeholder" : "Input your email here"})
    phone = StringField("Phone", validators=[
        Optional(), 
        Regexp("^[0-9]{10}$" ,  message='Must be a 10 digit phone number starting with area code')] ,
        render_kw={"placeholder" : "Input you 10 digit phone number here, starting with area code"})
    description = TextAreaField("Description" , validators=[Optional()] , render_kw={"placeholder" : "Input your description here"})
    image = FileField(
        "Image Upload" , 
        validators=[Optional()] ,
        render_kw={"placeholder" : "Upload your profile image. jpg, png, jpeg, gif only"})
    is_provider = BooleanField("Provider")
    calendar_email = EmailField(
        "Email for Google Calendar" , 
        validators=[Optional() , Length(min=1 , max=50) , Email(message='Must be a valid Gmail email address')],
        render_kw={"placeholder":"Input your gmail account here for calendar sharing. Providers only!"})
    is_active = BooleanField('Active')
