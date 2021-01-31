from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField , TextAreaField , SelectField , BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email , Length , Optional


class AdminLoginForm(FlaskForm):
    """Form for admin login"""
    username = StringField("Username", validators=[InputRequired(), Length(min=3 , max=20)], render_kw={"placeholder" : "Input your username here, must be between 3 to 20 letters or numbers"})
    password = PasswordField("Password", validators=[InputRequired()] , render_kw={"placeholder": "Input your password here"})
   
class AdminForm(FlaskForm):
    """Form for insert and update admin"""
    username = StringField("Username", validators=[InputRequired(), Length(min=3 , max=20)], render_kw={"placeholder" : "Input your username here, must be between 3 to 20 letters or numbers"})
    password = PasswordField("Password", validators=[InputRequired()] , render_kw={"placeholder": "Input your password here"})
    password_edit = PasswordField("Password", validators=[Optional()] , render_kw={"placeholder": "Input your password here"})
    first_name = StringField("First Name" , validators=[InputRequired() ,  Length(min=1 , max=30)], render_kw={"placeholder" : "Input your first name here"})
    last_name = StringField("Last Name" , validators=[InputRequired() , Length(min=1 , max=30)] , render_kw={"placeholder" : "Input your last name here"})
    email = EmailField("Email" , validators=[InputRequired() , Length(min=1 , max=50) , Email(message='Must be a valid email address')] , render_kw={"placeholder" : "Input your email here"})
    authorization = SelectField('Role' , choices=[('regular' , 'Regular') , ('administrator' , 'Administrator')])
    is_active = BooleanField('Active')
    