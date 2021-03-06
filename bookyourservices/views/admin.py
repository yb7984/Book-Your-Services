from flask import Blueprint, render_template, g, request, flash, url_for, jsonify
from utils import *
from forms import *
from models import *
from sqlalchemy.exc import IntegrityError
from views.modules.admin import AdminHandler
from views.modules.user import UserHandler
from views.modules.service import ServiceHandler
from views.modules.category import CategoryHandler
from google_calendar.google_calendar import GoogleCalendarHandler


admin = Blueprint('admin', __name__)

############
# filters for displaying on templates


@admin.app_template_filter('dt')
def _jinja2_filter_datetime(dt):

    return dt.strftime(DATETIME_FORMAT)


@admin.app_template_filter('d')
def _jinja2_filter_date(d):

    return dt.strftime(DATE_FORMAT)

###########
# Common methods


def login_admin_required(func):
    """
    For the route need to login as admin
    Check if the username in session
    Redirect to login page if not login yet
    """

    @wraps(func)
    def func_wrapper(*args, **kwargs):
        if login_admin_username() is None:
            flash("Please login first!", FLASH_GROUP_DANGER)
            return redirect(f'{url_for("admin.login")}?path={urllib.parse.quote_plus(request.path)}')

        return func(*args, **kwargs)

    return func_wrapper


def login_administrator_only(func):
    """
    For the route need to login as admin
    Check if the username in session
    Redirect to login page if not login yet
    Check if the authorization is administrator
    if not redirect to index page
    """
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        if login_admin_username() is None:
            flash("Please login first!", FLASH_GROUP_DANGER)
            return redirect(f'{url_for("admin.login")}?path={urllib.parse.quote_plus(request.path)}')

        if g.admin.authorization != ADMIN_AUTH_VALUE:
            flash("Not authorized visit!", FLASH_GROUP_DANGER)
            return redirect(url_for('admin.index'))

        return func(*args, **kwargs)

    return func_wrapper


def login_admin_username():
    """Return current login username of admin"""
    return session.get(ADMIN_USER_SESSION_KEY, None)


def login_admin_username_set(username):
    """Set current login username of admin"""

    session[ADMIN_USER_SESSION_KEY] = username

##################
# Methods for before request


@admin.before_request
def before_request_func():
    """Set current login user information"""

    if login_admin_username():
        g.admin = Admin.query.get(login_admin_username())

        if g.admin is None:
            flash("Please login first!", FLASH_GROUP_DANGER)
            session.clear()
            return redirect(f'{url_for("admin.login")}?path={urllib.parse.quote_plus(request.path)}')

        g.is_administrator = (g.admin.authorization == ADMIN_AUTH_VALUE)


#################
# Views

@admin.route('/admin')
@login_admin_required
def index():
    """Homepage for the admin"""

    return render_template('admin/index.html')


######
# For administrator accounts
#
@admin.route('/admin/login', methods=['POST', 'GET'])
def login():
    """login for admin"""

    if (login_admin_username()):
        # already login
        return redirect(url_for("admin.index"))

    form = AdminLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = Admin.authenticate(username, password)

        if user:
            flash(f"Welcome Back, {user.full_name}!", FLASH_GROUP_SUCCESS)

            login_admin_username_set(username)

            return redirect(url_for('admin.index'))
        else:
            flash('Invalid username/password.', 'danger')

    return render_template('admin/login.html', form=form)


@admin.route('/admin/logout', methods=['POST'])
@login_admin_required
def logout():
    """logout for admin"""

    session.clear()

    return redirect(url_for('admin.login'))


@admin.route('/admin/admins')
@login_administrator_only
def admins_list():
    """Show all the administators"""

    list = Admin.query.filter(Admin.is_active == True).all()

    list_inactive = Admin.query.filter(Admin.is_active == False).all()

    return render_template('admin/admins/list.html', list=list, list_inactive=list_inactive)


@admin.route('/admin/admins/new', methods=['POST', 'GET'])
@login_administrator_only
def admins_new():
    """New Administrator Account"""

    form = AdminForm()

    form_hide_value(form.password_edit, '')
    form_hide_value(form.is_active, True)

    if form.validate_on_submit():

        account = AdminHandler.register(form)

        if account is not None:
            flash('Successfully Created New Account!', FLASH_GROUP_SUCCESS)

            return redirect(url_for("admin.admins_list"))

    return render_template('admin/admins/new.html', form=form)


@admin.route('/admin/admins/<string:username>/update', methods=['POST', 'GET'])
@login_administrator_only
def admins_update(username):
    """Edit Administrator Account"""

    account = Admin.query.get_or_404(username)

    form = AdminForm(obj=account)
    form_hide_value(form.username, account.username)
    form_hide_value(form.password, account.password)

    if account.username == 'admin' or account.username == g.admin.username:
        # can not update the role for self or admin account
        form_hide_value(form.authorization, account.authorization)
        form_hide_value(form.is_active, True)

    if form.validate_on_submit():

        account = AdminHandler.update(account , form)

        if len(form.errors) == 0:
            flash('Successfully Update Account!', FLASH_GROUP_SUCCESS)

            return redirect(url_for("admin.admins_list"))

    return render_template('admin/admins/edit.html', form=form, account=account)



@admin.route('/admin/admins/password', methods=['POST', 'GET'])
@login_administrator_only
def admins_password_update():
    """Edit Password"""

    form = PasswordForm()

    if form.validate_on_submit():
        password = form.password.data

        account = Admin.update_password(login_admin_username() , password)

        if account != False:
            flash('Successfully Update Password!', FLASH_GROUP_SUCCESS)

            return redirect(url_for("admin.admins_password_update"))

    return render_template('admin/admins/password.html', form=form, account=g.admin)

@admin.route('/admin/admins/password_reset', methods=['POST', 'GET'])
def admins_password_reset():
    """Reset Password"""

    token = request.args.get('token' , None)

    if token is None:
        form = PasswordResetEmailForm()

        if form.validate_on_submit():
            if AdminHandler.reset_password_email(form):

                flash('The reset email has been sent to you email address!' , FLASH_GROUP_SUCCESS)
                return redirect(url_for('admin.login'))

            flash('Email is not found!' , FLASH_GROUP_DANGER)

        return render_template('admin/admins/password_reset.html' , form=form)
    
    # Set the new password
    form = PasswordResetForm()

    if form.validate_on_submit():
        
        account = AdminHandler.reset_password(form=form, token=token)

        if account:
            flash('Successfully reset password!' , FLASH_GROUP_SUCCESS)

            login_admin_username_set(account.username)

            return redirect(url_for('admin.index'))
        
        flash('Error when updating password!' , FLASH_GROUP_DANGER)

    return render_template('admin/admins/password_reset.html' , form=form)


@admin.route('/admin/admins/<string:username>/delete', methods=['POST'])
@login_administrator_only
def admins_delete(username):
    """Delete account"""

    if g.admin.username == username:
        flash('Unable to delete your own account!', 'danger')
        return redirect(url_for("admin.admins_list"))

    if username == 'admin':
        flash('Unable to delete admin account!', 'danger')
        return redirect(url_for("admin.admins_list"))

    AdminHandler.delete(username)

    flash('Successfull deactivate a account!', 'success')

    return redirect(url_for("admin.admins_list"))


######
# For website users account
#
@admin.route('/admin/users')
@login_admin_required
def users_list():
    """Show all the providers or customers"""

    pagination = UserHandler.list()

    return render_template('admin/users/list.html', pagination=pagination)


@admin.route('/admin/users/<string:username>')
@login_admin_required
def users_get(username):
    """Get user information detail"""

    account = User.query.get_or_404(username)

    service_form = ServiceForm(prefix="service")
    service_form.category_ids.choices = CategoryHandler.list_for_select()

    return render_template('admin/users/get.html',
                           account=account,
                           service_form=service_form)


@admin.route('/admin/users/new', methods=['POST', 'GET'])
@login_admin_required
def users_new():
    """New User Account"""

    form = UserForm()
    form_hide_value(form.password_edit, '')
    form_hide_value(form.is_active, True)

    if form.validate_on_submit():
        new_account = UserHandler.register(form)

        if new_account is not None:
            flash('Successfully Created New User!', FLASH_GROUP_SUCCESS)
            return redirect(url_for("admin.users_get", username=new_account.username))

    return render_template('admin/users/new.html', form=form)


@admin.route('/admin/users/<string:username>/update', methods=['POST', 'GET'])
@login_admin_required
def users_update(username):
    """Edit User Account"""

    user = User.query.get_or_404(username)

    form = UserForm(obj=user)

    form_hide_value(form.username, user.username)
    form_hide_value(form.password, user.password)

    if form.validate_on_submit():
        user = UserHandler.update(user, form)

        if len(form.errors) == 0:
            #no error, redirect
            flash('Successfully Update Account!', FLASH_GROUP_SUCCESS)

            return redirect(url_for("admin.users_get", username=username))

    return render_template('admin/users/edit.html', form=form, account=user)

@admin.route('/admin/users/<string:username>/delete', methods=['POST'])
@login_admin_required
def users_delete(username):
    """Delete account"""

    UserHandler.delete(username)

    flash('Successfull deactivate a user account!', 'success')

    return redirect(url_for("admin.users_list"))

######
# For Google Calendar
#
@admin.route('/admin/google_calendars', methods=['GET'])
@login_admin_required
def google_calendars_list():
    """Show google calendar list"""

    list = GoogleCalendarHandler.calendars_list()

    for item in list:
        calendar_id = item["id"]

        item["user"] = User.query.filter(User.calendar_id==calendar_id).first()

    return render_template("admin/google_calendars/list.html" , list=list)


@admin.route('/admin/google_calendars/<string:calendar_id>/delete', methods=['POST'])
@login_admin_required
def google_calendars_delete(calendar_id):
    """Show google calendar list"""

    GoogleCalendarHandler.calendars_delete(calendar_id)

    flash("Successfully deleted a google calendar!" , FLASH_GROUP_SUCCESS)

    return redirect(url_for('admin.google_calendars_list'))

######
# For services
#
@admin.route('/admin/users/<string:username>/services', methods=['GET'])
@login_admin_required
def services_list(username):
    """Get Service List"""

    items = ServiceHandler.list_by_username(username)

    return jsonify(items=[item.serialize() for item in items])


@admin.route('/admin/users/<string:username>/services/<int:service_id>', methods=['GET'])
@login_admin_required
def services_get(username, service_id):
    """Get Service"""
    item = Service.query.get(service_id)

    if item is None:
        return ("", 404)

    return jsonify(item=item.serialize())


@admin.route('/admin/users/<string:username>/services', methods=['POST'])
@login_admin_required
def services_new(username):
    """New Service"""

    item = ServiceHandler.insert(username)

    if "item" in item:
        return (jsonify(item) , 201)

    return (jsonify(item) , 200)

@admin.route('/admin/users/<string:username>/services/<int:service_id>', methods=['PATCH'])
@login_admin_required
def services_update(username, service_id):
    """Update Service"""

    item = ServiceHandler.update(service_id)

    return (jsonify(item) , 200)


@admin.route('/admin/users/<string:username>/services/<int:service_id>', methods=['DELETE'])
@login_admin_required
def services_delete(username, service_id):
    """Delete Service"""

    return (jsonify(ServiceHandler.delete(service_id)) , 200)

######
# For categories
#
@admin.route('/admin/categories/index')
def categories_index():
    """Page for categories management"""
    form = CategoryForm()

    return render_template('admin/categories/index.html', form=form)

@admin.route('/admin/categories')
@login_admin_required
def categories_list():
    """Show all the categories"""

    items = CategoryHandler.list()

    return jsonify(items=[item.serialize() for item in items])


@admin.route('/admin/categories', methods=['POST'])
@login_admin_required
def categories_new():
    """New Category"""

    item = CategoryHandler.insert()

    if "item" in item:
        return (jsonify(item) , 201)

    return (jsonify(item) , 200)


@admin.route('/admin/categories/<int:category_id>', methods=['PATCH'])
@login_admin_required
def categories_update(category_id):
    """Edit Category"""

    item = CategoryHandler.update(category_id)

    return (jsonify(item) , 200)


@admin.route('/admin/categories/<int:category_id>', methods=['DELETE'])
@login_admin_required
def categories_delete(category_id):
    """Delete category"""

    return (jsonify(CategoryHandler.delete(category_id)) , 200)
