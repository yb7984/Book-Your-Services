from flask import Blueprint, render_template , g , request , flash , url_for
from google_calendar.google_calendar import *
from secrets import token_urlsafe
from utils import *
from forms.admins import * 
from forms.users import *
from forms.categories import *
from models import *
from sqlalchemy.exc import IntegrityError

admin = Blueprint('admin', __name__)

############
#filters for displaying on templates
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
    def func_wrapper(*args , **kwargs):
        if login_admin_username() is None:
            flash("Please login first!", "danger")
            return redirect(f'/admin/login?path={urllib.parse.quote_plus(request.path)}')

        return func(*args , **kwargs)

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
    def func_wrapper(*args , **kwargs):
        if login_admin_username() is None:
            flash("Please login first!", "danger")
            return redirect(f'{url_for("admin.login")}?path={urllib.parse.quote_plus(request.path)}')

        if g.admin.authorization != "administrator":
            flash("Not authorized visit!", "danger")
            return redirect(url_for('admin.index'))

        return func(*args , **kwargs)

    return func_wrapper

def login_admin_username():
    """Return current login username of admin"""
    return session.get(ADMIN_USER_SESSION_KEY , None)

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


#################
# Views

@admin.route('/admin')
@login_admin_required
def index():
    """Homepage for the admin"""

    return render_template('admin/index.html')


@admin.route('/admin/login' , methods=['POST' , 'GET'])
def login():
    """login for admin"""

    if (login_admin_username()):
        #already login
        return redirect(url_for("admin.index"))

    form = AdminLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = Admin.authenticate(username, password)

        if user:
            flash(f"Welcome Back, {user.full_name}!", "success")

            login_admin_username_set(username)

            return redirect(url_for('admin.index'))
        else:
            flash('Invalid username/password.' , 'danger')

    return render_template('admin/login.html', form=form)

@admin.route('/admin/logout' , methods=['POST'])
@login_admin_required
def logout():
    """logout for admin"""

    session.clear()

    return redirect(url_for('admin.login'))

@admin.route('/admin/admins')
@login_administrator_only
def admins_list():
    """Show all the administators"""
        
    list = Admin.query.filter(Admin.is_active==True).all()
        
    list_inactive = Admin.query.filter(Admin.is_active==False).all()

    return render_template('admin/admins/list.html' , list=list , list_inactive=list_inactive)



@admin.route('/admin/admins/new' , methods=['POST' , 'GET'])
@login_administrator_only
def admins_new():
    """New Administrator Account"""
    
    form = AdminForm()

    form_hide_value(form.password_edit , '')
    form_hide_value(form.is_active , True)

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data 

        new_account = Admin.register(username, password , email , first_name , last_name)
        new_account.authorization = form.authorization.data

        db.session.add(new_account)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            form.username.errors.append('Username or Email taken.  Please pick another')
            return render_template('admin/admins/new.html', form=form)
        except:
            db.session.rollback()
            form.username.errors.append('Username or Email taken.  Please pick another')
            return render_template('admin/admins/new.html', form=form)


        flash('Successfully Created New Account!', "success")

        return redirect(url_for("admin.admins_list"))

    return render_template('admin/admins/new.html', form=form)


@admin.route('/admin/admins/<string:username>/update' , methods=['POST' , 'GET'])
@login_administrator_only
def admins_update(username):
    """Edit Administrator Account"""

    account = Admin.query.get_or_404(username)

    form = AdminForm(obj=account)
    form_hide_value(form.username , account.username)
    form_hide_value(form.password , account.password)

    if account.username == 'admin' or account.username == g.admin.username:
        #can not update the role for self or admin account
        form_hide_value(form.authorization , account.authorization)
        form_hide_value(form.is_active , True)

    if form.validate_on_submit():
        password = form.password.data

        if len(password) > 0:
            account.password = hash_password(password)

        account.email = form.email.data
        account.first_name = form.first_name.data
        account.last_name = form.last_name.data 

        if account.username != 'admin':
            #can not update the role for the admin account
            account.authorization = form.authorization.data
            account.is_active = form.is_active.data
        else :
            account.authenticate = ADMIN_AUTH_VALUE
            account.is_active = True
        
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username or Email taken.  Please pick another')
            return render_template('admin/admins/edit.html', form=form , account=account)

        flash('Successfully Update Account!', "success")

        return redirect(url_for("admin.admins_list"))

    return render_template('admin/admins/edit.html', form=form , account=account)



@admin.route('/admin/admins/<string:username>/delete' , methods=['POST'])
@login_administrator_only
def admins_delete(username):
    """Delete account"""

    if g.admin.username == username:
        flash('Unable to delete your own account!' , 'danger')
        return redirect(url_for("admin.admins_list"))

    if username == 'admin':
        flash('Unable to delete admin account!' , 'danger')
        return redirect(url_for("admin.admins_list"))

    account = Admin.query.get_or_404(username)

    account.is_active = False

    db.session.commit()

    flash('Successfull deactivate a account!' , 'success')

    return redirect(url_for("admin.admins_list"))

@admin.route('/admin/users')
@login_admin_required
def users_list():
    """Show all the providers or customers"""

    page = int(request.args.get("page" , 1))

    username = request.args.get('username' , '')
    email = request.args.get('email' , '')
    is_provider = request.args.get('is_provider' , '')
    is_active = request.args.get('is_active' , '')

    filters = []
    if len(username) > 0:
        filters.append(User.username.like(f'%{username}%'))
    
    if len(email) > 0:
        filters.append(User.email.like(f'%{email}%'))
    if len(is_provider) > 0:
        filters.append(User.is_provider==(True if is_provider=='1' else False))
    if len(is_active) > 0:
        filters.append(User.is_active==(True if is_active=='1' else False))

    pagination = User.query.filter(*tuple(filters)).paginate(page , per_page=ADMIN_USERS_PER_PAGE)

    return render_template('admin/users/list.html' , pagination=pagination)

@admin.route('/admin/users/<string:username>')
@login_admin_required
def users_get(username):
    """Get user information detail"""

    account = User.query.get_or_404(username)

    return render_template('admin/users/get.html' , account=account)

@admin.route('/admin/users/new' , methods=['POST' , 'GET'])
@login_admin_required
def users_new():
    """New User Account"""
    
    form = UserForm()
    form_hide_value(form.password_edit , '')
    form_hide_value(form.is_active , True)
    
    if form.validate_on_submit():
        username = form.username.data.lower().strip()
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data 
        is_provider = form.is_provider.data

        new_account = User.register(username, password , email , first_name , last_name , is_provider)

        new_account.phone = form.phone.data
        new_account.description = form.description.data

        #todo create a calendar and share if calendar_email is not empty
        if is_provider:
            new_account.calendar_email = form.calendar_email.data

        db.session.add(new_account)

        try:
            db.session.commit()

            #upload file
            image = upload_file(
                form.image.name , 
                name=username ,
                dirname=USER_UPLOAD_DIRNAME , 
                exts=IMAGE_ALLOWED_EXTENSIONS)


            if image is not None:
                new_account.image = image
                #update the image information
                db.session.commit()

        except IntegrityError:
            db.session.rollback()
            form.username.errors.append('Username or Email taken.  Please pick another')
            return render_template('admin/users/new.html', form=form)
        except:
            db.session.rollback()
            form.username.errors.append('Username or Email taken.  Please pick another')
            return render_template('admin/users/new.html', form=form )


        flash('Successfully Created New User!', "success")

        return redirect(url_for("admin.users_get" , username=username))

    return render_template('admin/users/new.html', form=form)


@admin.route('/admin/users/<string:username>/update' , methods=['POST' , 'GET'])
@login_admin_required
def users_update(username):
    """Edit User Account"""

    account = User.query.get_or_404(username)

    form = UserForm(obj=account)
    
    form_hide_value(form.username , account.username)
    form_hide_value(form.password , account.password)


    if form.validate_on_submit():
        password = form.password_edit.data

        if len(password) > 0:
            account.password = hash_password(password)

        account.email = form.email.data
        account.first_name = form.first_name.data
        account.last_name = form.last_name.data 
        account.is_active = form.is_active.data

        account.phone = form.phone.data
        account.description = form.description.data

        account.is_provider = form.is_provider.data

        account.updated = datetime.datetime.now()

        #todo create a calendar and share if calendar_email is not empty
        if account.is_provider:
            account.calendar_email = form.calendar_email.data
        else:
            account.calendar_email = None

        try:
            db.session.commit()

            #upload file
            image = upload_file(
                form.image.name , 
                name=username ,
                dirname=USER_UPLOAD_DIRNAME , 
                exts=IMAGE_ALLOWED_EXTENSIONS)

            if image is not None:
                account.image = image
                #update the image information
                db.session.commit()

        except IntegrityError:
            form.username.errors.append('Username or Email taken.  Please pick another')
            return render_template('admin/users/edit.html', form=form , account=account , fields_disabled=fields_disabled)

        flash('Successfully Update Account!', "success")

        return redirect(url_for("admin.users_get" , username=username))

    return render_template('admin/users/edit.html', form=form , account=account)



@admin.route('/admin/users/<string:username>/delete' , methods=['POST'])
@login_admin_required
def users_delete(username):
    """Delete account"""

    account = User.query.get_or_404(username)

    account.is_active = False

    db.session.commit()

    flash('Successfull deactivate a user account!' , 'success')

    return redirect(url_for("admin.users_list"))


@admin.route('/admin/categories')
@login_admin_required
def categories_list():
    """Show all the categories"""

    list = Category.query.all()

    return render_template('admin/categories/list.html' , list=list)

@admin.route('/admin/categories/new' , methods=['POST' , 'GET'])
@login_admin_required
def categories_new():
    """New Category"""
    
    form = CategoryForm()
    form_hide_value(form.is_active , True)
    
    if form.validate_on_submit():
        name = form.name.data

        category = Category(name=name)

        db.session.add(category)

        try:
            db.session.commit()

        except:
            db.session.rollback()
            flash('Error when adding a category' , 'danger')

            return render_template('admin/categories/new.html', form=form)


        flash('Successfully Created New Category!', "success")

        return redirect(url_for("admin.categories_list"))

    return render_template('admin/categories/new.html', form=form)



@admin.route('/admin/categories/<int:id>/update' , methods=['POST' , 'GET'])
@login_admin_required
def categories_update(id):
    """Edit Category"""

    category = Category.query.get_or_404(id)

    form = CategoryForm(obj=category)
    
    if form.validate_on_submit():
        category.name = form.name.data
        category.is_active = form.is_active.data

        try:
            db.session.commit()

        except:
            db.session.rollback()
            flash('Error when updating a category' , 'danger')

            return render_template('admin/categories/edit.html', form=form)


        flash('Successfully Updated Category!', "success")

        return redirect(url_for("admin.categories_list"))

    return render_template('admin/categories/edit.html', form=form)

@admin.route('/admin/categories/<int:id>/delete' , methods=['POST'])
@login_admin_required
def categories_delete(id):
    """Delete category"""

    category = Category.query.get_or_404(id)

    category.is_active = False

    db.session.commit()

    flash('Successfull deactive a category!' , 'success')

    return redirect(url_for("admin.categories_list"))
