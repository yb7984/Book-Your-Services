"""Modules file for handling request related to user"""

from models import User, db
from flask import request, jsonify, url_for
from forms import UserForm, UserLoginForm
from utils import *
from google_calendar.google_calendar import GoogleCalendarHandler
import datetime
from secrets import token_urlsafe


class UserHandler:
    """Handler for user"""

    @staticmethod
    def list(only_active=False, provider_only=False, per_page=ADMIN_USERS_PER_PAGE):
        """Return user list"""
        page = int(request.args.get("page", 1))
        username = request.args.get('username', '')
        email = request.args.get('email', '')
        is_provider = request.args.get('is_provider', '')
        is_active = request.args.get('is_active', '')
        term=request.args.get('term', '')

        limit = int(request.args.get("limit" , -1))
        if limit > 0:
            per_page = limit
        else:
            limit = int(request.args.get("per_page" , -1))
            if limit > 0:
                per_page = limit

        if only_active == True:
            is_active = "1"

        filters = []

        if len(term) > 0:
            filters.append(
                User.username.like(f'%{term}%') |
                User.first_name.like(f'%{term}%') |
                User.last_name.like(f'%{term}%') |
                User.email.like(f'%{term}%')  |
                User.description.like(f'%{term}%') 
                )

        if len(username) > 0:
            filters.append(User.username.like(f'%{username}%'))

        if len(email) > 0:
            filters.append(User.email.like(f'%{email}%'))

        if provider_only == False:
            if len(is_provider) > 0:
                filters.append(User.is_provider == (
                    True if is_provider == '1' else False))
        else:
            filters.append(User.is_provider==True)

        if only_active == False:
            if len(is_active) > 0:
                filters.append(User.is_active == (
                    True if is_active == '1' else False))
        else:
            filters.append(User.is_active==True)

        return User.query.filter(
            *tuple(filters)).paginate(page, per_page=per_page)

    @staticmethod
    def get(username):
        """Return User"""
        return User.query.get(username)

    @staticmethod
    def register(form):
        """New User"""
        username = form.username.data.lower().strip()
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        is_provider = form.is_provider.data

        # check duplicate username and email
        count = User.query.filter(User.username == username).count()

        if count > 0:
            form.username.errors.append(
                'Username taken.  Please pick another')

        count = User.query.filter(User.email == email).count()

        if count > 0:
            form.email.errors.append(
                'Email taken.  Please pick another')

        if len(form.errors) > 0:
            return None

        user = User.register(
            username, password, email, first_name, last_name, is_provider)

        user.phone = form.phone.data
        user.description = form.description.data

        db.session.add(user)

        success = False
        # try:
        db.session.commit()

        success = True

        # except IntegrityError:
        #     db.session.rollback()
        #     form.username.errors.append(
        #         'Username or Email taken.  Please pick another')

        #     return None
        # except:
        #     db.session.rollback()
        #     form.username.errors.append(
        #         'Username or Email taken.  Please pick another')

        #     return None

        if success == True:

            # upload file
            UserHandler.upload_image(user, form)

            # setup google calendar
            UserHandler.set_google_calendar(user , form)

            return user

        return None

    @staticmethod
    def update(user, form):
        """Update Useres"""

        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.is_active = form.is_active.data
        user.phone = form.phone.data
        user.description = form.description.data
        user.is_provider = form.is_provider.data

        password = form.password_edit.data

        if len(password) > 0:
            user.password = hash_password(password)

        if user.email != form.email.data:
            # check duplicate username and email
            user.email = form.email.data
            count = User.query.filter(
                User.email == user.email, User.username != user.username).count()
            if count > 0:
                form.email.errors.append(
                    'Email taken.  Please pick another')
                return user

        user.updated = datetime.datetime.now()

        success = False
        try:
            db.session.commit()
            success = True
        except IntegrityError:
            form.email.errors.append(
                'Email taken.  Please pick another')

            return user

        if success == True:
            #upload image
            UserHandler.upload_image(user, form)

            # setup google calendar
            UserHandler.set_google_calendar(user , form)

        return user

    @staticmethod
    def delete(username):
        """Delete Useres"""
        user = User.query.get(username)

        if user is None:
            return {}

        user.is_active = False

        db.session.commit()

        return {}


    
    @staticmethod
    def reset_password_email(form):
        """For reset password, if found the account return true"""
        
        email = form.email.data

        account = User.query.filter(User.email == email).first()

        if account:
            account.pwd_token = token_urlsafe()
            db.session.commit()

            mail.send_message(
                subject='Book your services admin password reset' ,
                sender='bobowu98@gmail.com',
                recipients=[email] ,
                body=f'{BASE_URL}{url_for("home.password_reset")}?token={account.pwd_token}'
            )

            return True
        return False

    
    @staticmethod
    def reset_password(form , token):
        """For reset password"""
        
        password = form.password.data

        return User.update_password_by_token(token=token , password=password)

    @staticmethod
    def upload_image(user, form):
        """upload user image"""
        # upload file
        image = upload_file(
            form.image.name,
            name=user.username,
            dirname=upload_dir_user(user.username),
            exts=IMAGE_ALLOWED_EXTENSIONS)

        if image is not None:
            user.image = image
            # update the image information
            db.session.commit()

    @staticmethod
    def set_google_calendar(user, form):
        """Set the google calendar for provider"""

        if user.is_provider and form.calendar_email.data.strip() != "":
            #if is provider and providing the gmail account, create the calendar and share

            if user.calendar_id is None or user.calendar_id.strip() == "":
                # calendar not created, create it

                calendar = GoogleCalendarHandler.calendars_insert(
                    summary=f"{user.full_name}'s calendar",
                    description=f"Book your services calendar for {user.full_name}")

                if calendar is not None:
                    user.calendar_id = calendar["id"]

            if user.calendar_email != form.calendar_email.data.strip().lower():
                # calendar_email is different, create the share
                if user.calendar_email is not None or user.calendar_email != "":
                    #got the share before, delete the original share first
                    GoogleCalendarHandler.calendars_share_delete(user.calendar_id , user.calendar_email)

                #set the new email and share
                user.calendar_email = form.calendar_email.data.strip().lower()
                GoogleCalendarHandler.calendars_share(user.calendar_id , user.calendar_email)

        elif user.is_provider == False:
            user.calendar_email = None

        
        db.session.commit()

            



