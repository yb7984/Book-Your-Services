from flask import Blueprint, render_template, g, request, flash, url_for, jsonify
from secrets import token_urlsafe
from utils import *
from forms import *
from models import *
from views.modules.user import UserHandler
from views.modules.service import ServiceHandler
from views.modules.category import CategoryHandler
from views.modules.schedule import ScheduleHandler
from google_calendar.google_calendar import GoogleCalendarHandler


home = Blueprint('home', __name__)


############
# filters for displaying on templates


@home.app_template_filter('dt')
def _jinja2_filter_datetime(dt):

    return dt.strftime(DATETIME_FORMAT)


@home.app_template_filter('d')
def _jinja2_filter_date(d):

    return dt.strftime(DATE_FORMAT)


###########
# User Login methods


def login_required(func):
    """
    For the route need to login
    Check if the username in session
    Redirect to login page if not login yet
    """

    @wraps(func)
    def func_wrapper(*args, **kwargs):
        if login_username() is None:
            flash("Please login first!", FLASH_GROUP_DANGER)
            return redirect(f'{url_for("home.login")}?path={urllib.parse.quote_plus(request.path)}')

        return func(*args, **kwargs)

    return func_wrapper


##################
# Methods for before request


@home.before_request
def before_request_func():
    """Set current login user information"""

    g.global_values = {}

    if login_username():
        g.user = User.query.get(login_username())

        if g.user is not None:
            g.global_values["CURRENT_USERNAME"] = g.user.username

        if g.user is None:
            flash("Please login first!", FLASH_GROUP_DANGER)
            session.clear()
            return redirect(f'{url_for("home.login")}?path={urllib.parse.quote_plus(request.path)}')


@home.route('/')
def index():
    # Do some stuff

    service_form = ServiceSearchForm()
    service_form.categories.choices.extend(CategoryHandler.list_for_select())
    service_url = "/services"

    provider_form = BaseSearchForm()
    provider_url = "/providers"

    appointment_form = AppointmentForm(prefix="appointment")

    return render_template("home/index.html",
                           service_url=service_url,
                           service_form=service_form,
                           provider_url=provider_url,
                           provider_form=provider_form,
                           appointment_form=appointment_form)


@home.route('/services')
def services_list():
    """Service List"""

    service_form = ServiceSearchForm()
    service_form.categories.choices.extend(CategoryHandler.list_for_select())
    service_url = "/services"

    service_form.term.data = request.args.get("term", "")
    service_form.categories.data = request.args.get("categories", "0")

    appointment_form = AppointmentForm(prefix="appointment")

    return render_template("home/services.html",
                           service_url=service_url,
                           service_form=service_form,
                           appointment_form=appointment_form)


@home.route('/providers')
def providers_list():
    """Provider List"""

    provider_form = BaseSearchForm()
    provider_url = "/providers"

    provider_form.term.data = request.args.get("term", "")

    return render_template("home/providers.html",
                           provider_url=provider_url,
                           provider_form=provider_form)


@home.route('/providers/<string:username>')
def provider_detail(username):
    """Provider Detail"""

    user = User.query.get_or_404(username)

    g.global_values["PROVIDER_USERNAME"] = user.username

    return render_template("home/provider.html", account=user)


######
# For user accounts
#
@home.route('/login', methods=['POST', 'GET'])
def login():
    """login"""

    if (login_username()):
        # already login
        return redirect(url_for("home.dashboard"))

    form = UserLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            flash(f"Welcome Back, {user.full_name}!", FLASH_GROUP_SUCCESS)

            login_username_set(username)

            path = request.args.get("path", "")

            if path == "":
                return redirect(url_for('home.dashboard'))
            else:
                return redirect(path)
        else:
            flash('Invalid username/password.', 'danger')

    return render_template('home/users/login.html', form=form)


@home.route('/register', methods=['POST', 'GET'])
def register():
    """New User Account"""

    form = UserForm()
    form_hide_value(form.password_edit, '')
    form_hide_value(form.first_name, '')
    form_hide_value(form.last_name, '')
    form_hide_value(form.description, '')
    form_hide_value(form.phone, '')
    form_hide_value(form.image, '')
    form_hide_value(form.is_active, True)

    if form.validate_on_submit():
        new_account = UserHandler.register(form)

        if new_account is not None:
            # login the new account and redirect to dashboard
            login_username_set(new_account.username)

            flash('Successfully Registered!', FLASH_GROUP_SUCCESS)
            return redirect(url_for("home.dashboard"))

    return render_template('home/users/register.html', form=form)


@home.route('/password_reset', methods=['POST', 'GET'])
def password_reset():
    """Reset Password"""

    token = request.args.get('token', None)

    if token is None:
        form = PasswordResetEmailForm()

        if form.validate_on_submit():
            if UserHandler.reset_password_email(form):

                flash('The reset email has been sent to you email address!',
                      FLASH_GROUP_SUCCESS)
                return redirect(url_for('home.login'))

            flash('Email is not found!', FLASH_GROUP_DANGER)

        return render_template('home/users/password_reset.html', form=form)

    user = User.query.filter(User.pwd_token == token,
                             User.is_active == True).first()

    if user is None:

        flash('Invalid Token, please try again!', FLASH_GROUP_DANGER)

        return redirect(url_for("home.password_reset"))

    # Set the new password
    form = PasswordResetForm()

    if form.validate_on_submit():

        account = UserHandler.reset_password(form=form, token=token)

        if account:
            flash('Successfully reset password!', FLASH_GROUP_SUCCESS)

            login_username_set(account.username)

            return redirect(url_for('home.dashboard'))

        flash('Error when updating password!', FLASH_GROUP_DANGER)

    return render_template('home/users/password_reset.html', form=form)


@home.route('/logout', methods=['POST'])
def logout():
    """logout"""

    session.clear()

    return redirect(url_for('home.login'))


@home.route('/users/dashboard')
@login_required
def dashboard():
    """Get user dashboard"""

    g.global_values["PROVIDER_USERNAME"] = g.user.username
    g.global_values["APPOINTMENT_LIST_URL"] = f'/api/appointments/{ g.user.username }?{"is_provider=1" if g.user.is_provider else ""}'
    g.global_values["APPOINTMENT_UPDATE_URL"] = '/api/appointments/0'
    g.global_values["APPOINTMENT_DELETE_URL"] = '/api/appointments/0'
    g.global_values["APPOINTMENT_PER_PAGE"] = '6'

    appointment_form = AppointmentForm(prefix="appointment")

    service_form = ServiceForm(prefix="service")
    service_form.category_ids.choices = CategoryHandler.list_for_select()

    return render_template("home/users/dashboard.html", account=g.user,
                           appointment_form=appointment_form,
                           service_form=service_form)


@home.route('/users/profile')
@login_required
def profile():
    """Get user dashboard"""

    return render_template("home/users/profile.html", account=g.user)


@home.route('/users/edit', methods=['POST', 'GET'])
@login_required
def user_edit():
    """Get user dashboard"""

    user = g.user

    form = UserForm(obj=user)

    form_hide_value(form.username, user.username)
    form_hide_value(form.password, user.password)
    form_hide_value(form.password_edit, '')
    form_hide_value(form.is_active, True)

    if form.validate_on_submit():
        user = UserHandler.update(user, form)

        if len(form.errors) == 0:
            # no error, redirect
            flash('Successfully Update Account!', FLASH_GROUP_SUCCESS)

            return redirect(url_for("home.profile"))

    return render_template('home/users/edit.html', form=form, account=user)


@home.route('/users/password', methods=['POST', 'GET'])
@login_required
def password_update():
    """Edit Password"""

    form = PasswordForm()

    if form.validate_on_submit():
        password = form.password.data

        account = User.update_password(login_username(), password)

        if account != False:
            flash('Successfully Updated Password!', FLASH_GROUP_SUCCESS)

            return redirect(url_for("home.password_update"))

    return render_template('home/users/password.html', form=form, account=g.user)


@home.route('/users/myservices')
@login_required
def my_services():
    """Get all my services"""

    if not g.user.is_provider:
        flash("Unauthorized visit!", FLASH_GROUP_DANGER)

        return redirect(url_for("home.dashboard"))

    form = ServiceForm(prefix="service")
    form.category_ids.choices = CategoryHandler.list_for_select()

    return render_template("home/services/list.html", form=form)


@home.route('/users/myschedules')
@login_required
def my_schedules():
    """Get all my schedules"""

    if not g.user.is_provider:
        flash("Unauthorized visit!", FLASH_GROUP_DANGER)

        return redirect(url_for("home.dashboard"))

    form = ScheduleForm(prefix="schedule")

    return render_template("home/schedules/list.html", form=form)


@home.route('/users/myappointments')
@login_required
def my_appointments():
    """Get all my services"""

    g.global_values["APPOINTMENT_LIST_URL"] = f'/api/appointments/{login_username()}'
    g.global_values["APPOINTMENT_UPDATE_URL"] = '/api/appointments/0'
    g.global_values["APPOINTMENT_DELETE_URL"] = '/api/appointments/0'

    appointment_form = AppointmentForm(prefix="appointment")

    return render_template("home/appointments/list.html", form=appointment_form, is_past=bool(request.args.get("is_past", 0)))


@home.route('/users/provider_appointments')
@login_required
def provider_appointments():
    """Get all my services"""

    if not g.user.is_provider:
        flash("Unauthorized visit!", FLASH_GROUP_DANGER)

        return redirect(url_for("home.dashboard"))

    g.global_values["APPOINTMENT_LIST_URL"] = f'/api/appointments/{login_username()}?is_provider=1'
    g.global_values["APPOINTMENT_UPDATE_URL"] = '/api/appointments/0'
    g.global_values["APPOINTMENT_DELETE_URL"] = '/api/appointments/0'

    appointment_form = AppointmentForm(prefix="appointment")

    return render_template("home/appointments/list-provider.html", form=appointment_form, is_past=bool(request.args.get("is_past", 0)))
