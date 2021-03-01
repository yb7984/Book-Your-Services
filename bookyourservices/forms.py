from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField , TextAreaField , SelectField , BooleanField , FileField , HiddenField , SelectMultipleField , ValidationError, widgets
from wtforms.fields.html5 import EmailField , IntegerField, DateField, DateTimeField, TimeField
from wtforms.validators import InputRequired, Email , Length , Optional , Regexp, EqualTo
from config import *
import datetime

class CheckboxMultipleField(SelectMultipleField):
    """Multiple Checkbox field"""
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

######
# For Search
#
class BaseSearchForm(FlaskForm):
    """Basic Search Form"""

    class Meta:
        csrf = False  # Disable CSRF
    term = StringField("term", validators=[Optional()], render_kw={"placeholder" : "Start your search here"})
    
class ServiceSearchForm(BaseSearchForm):
    """Search form for Service"""
    
    categories = SelectField("Categories" , choices=[("0" , "All Categories")])
    


######
# For Admin
#
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
    

class PasswordForm(FlaskForm):
    """Form for changing password"""
    password = PasswordField("Password", validators=[InputRequired() , EqualTo("password_confirm" , message="Password must match")] , render_kw={"placeholder": "Input your password here"})
    password_confirm = PasswordField("Password Confirm" , render_kw={"placeholder": "Input your password confirm here"})
   
class PasswordResetEmailForm(FlaskForm):
    """Form for reset password email"""
    email = EmailField("Email" , validators=[InputRequired() , Length(min=1 , max=50) , Email(message='Must be a valid email address')] , render_kw={"placeholder": "Input your email with your account here"})
    

class PasswordResetForm(FlaskForm):
    """Form for reset password"""
    password = PasswordField("New Password", validators=[InputRequired()] , render_kw={"placeholder": "Input your new password here"})

######
# For User
#
class UserLoginForm(FlaskForm):
    """Form for admin login"""
    username = StringField("Username", validators=[InputRequired(), Length(min=3 , max=20)])
    password = PasswordField("Password", validators=[InputRequired()])

class UserForm(FlaskForm):
    """Form for insert/update user"""
    username = StringField("Username", validators=[InputRequired(), Length(min=3 , max=20)], render_kw={"placeholder" : "Input your username here, must be between 3 to 20 letters or numbers"})
    password = PasswordField("Password", validators=[InputRequired()] , render_kw={"placeholder": "Input your password here"})
    password_edit = PasswordField("Password", validators=[Optional()] , render_kw={"placeholder": "Input your password here"})
    first_name = StringField("First Name" , validators=[Optional() ,  Length(min=1 , max=30)], render_kw={"placeholder" : "Input your first name here"})
    last_name = StringField("Last Name" , validators=[Optional() , Length(min=1 , max=30)] , render_kw={"placeholder" : "Input your last name here"})
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


######
# For Address
#
class AddressForm(FlaskForm):
    """Form for insert/update address"""
    id = HiddenField("ID")
    username = HiddenField("Username")
    name = StringField("Name", validators=[InputRequired(), Length(min=1 , max=100)], render_kw={"placeholder" : "Input your name here"})
    address1 = StringField("Address1" , validators=[InputRequired() ,  Length(min=1 , max=100)], render_kw={"placeholder" : "Input your street address here"})
    address2 = StringField("Address2" , validators=[Optional() , Length(min=1 , max=100)] , render_kw={"placeholder" : "Input your unit number here"})
    city = StringField("City" , validators=[InputRequired() , Length(min=1 , max=50)] , render_kw={"placeholder" : "Input your city here"})
    state = SelectField("States" , choices=US_ABBREV_STATES.items())
    zipcode = StringField("ZipCode", validators=[
        InputRequired(), 
        Regexp("^[0-9]{5}$" ,  message='Must be a 5 digit zipcode')] ,
        render_kw={"placeholder" : "Input you 5 digit zipcode here"})
    is_default = BooleanField('Default')
    is_active = BooleanField('Active' , default=True)


######
# For Category
#
class CategoryForm(FlaskForm):
    """Form for insert / update categories"""
    id = HiddenField("ID")
    name = StringField("Name", validators=[InputRequired(), Length(min=1 , max=100)], render_kw={"placeholder" : "Input the category name here"})
    is_active = BooleanField('Active' , default=True)



######
# For Service
#
class ServiceForm(FlaskForm):
    """Form for insert/update service"""
    id = HiddenField("ID")
    username = HiddenField("Username")
    name = StringField("Name", validators=[InputRequired(), Length(min=1 , max=100)], render_kw={"placeholder" : "Input your service name here"})
    category_ids = CheckboxMultipleField("Categories" , choices=[])
    location_type = SelectField("Location" , choices=[(0 , "Online Service") , (1 , "Phone Service")])
    description = TextAreaField("Description", validators=[Optional()] ,
        render_kw={"placeholder" : "Input service description here" , 
        "rows": 6})
    image = FileField(
        "Image Upload" , 
        validators=[Optional()] ,
        render_kw={"placeholder" : "Upload your profile image. jpg, png, jpeg, gif only"})
    is_active = BooleanField('Active' , default=True)



######
# For Appointment
#
class AppointmentForm(FlaskForm):
    """Form for insert/update appointment"""
    id = HiddenField("ID")
    event_id = HiddenField("Event ID")
    service_id = HiddenField("Service")
    provider_username = HiddenField("Provider Username")
    customer_username = HiddenField("Customer Username")
    service_date = DateField("Service Date", validators=[InputRequired()] , render_kw={"placeholder":"Input your service date here"})
    start = TimeField("Starts from" , validators=[InputRequired()])
    end = TimeField("Ends at" , validators=[InputRequired()])
    note = TextAreaField("Note", validators=[Optional()] ,
        render_kw={"placeholder" : "Input your note here" , 
        "rows": 6})

    def validate_service_date(form, field):
        """validator for service_date"""
        if field.data < datetime.date.today():
            raise ValidationError("Service date can not be earlier than today!")

    def validate_start(form, field):
        """validator for start"""
        if datetime.datetime.combine(form.service_date.data , form.start.data) <= datetime.datetime.now():
            raise ValidationError("Start time must be later than now!")
    
    def validate_end(form, field):
        """validator for end"""
        if field.data <= form.start.data:
            raise ValidationError("End time must be later than start time!")





