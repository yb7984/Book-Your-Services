"""Modules file for handling request related to admin"""

from models import Admin, db
from flask import request , jsonify, url_for
from forms import AdminForm, AdminLoginForm
from utils import *
import datetime
from secrets import token_urlsafe

class AdminHandler:
    """Handler for admin"""

    @staticmethod
    def list(is_active=True):
        """Return admin list"""
        
        return Admin.query.filter(Admin.is_active == is_active).all()

    @staticmethod
    def get(username):
        """Return Admin"""
        return Admin.query.get(user_id)

    @staticmethod
    def register(form):
        """New Admin"""

        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        #check duplicate username and email
        count = Admin.query.filter(db.or_(Admin.username==username, Admin.email==email)).count()

        if count > 0:
            form.username.errors.append(
                'Username or Email taken.  Please pick another')

            return None

        new_account = Admin.register(
            username, password, email, first_name, last_name)

        new_account.authorization = form.authorization.data

        db.session.add(new_account)

        success = False
        try:
            db.session.commit()
            success = True

        except IntegrityError:
            db.session.rollback()
            form.username.errors.append(
                'Username or Email taken.  Please pick another')
                
            return None
        except:
            db.session.rollback()
            form.username.errors.append(
                'Username or Email taken.  Please pick another')
            
        
        if success == True:
            return new_account

        
        return None

    @staticmethod
    def update(admin, form):
        """Update Useres"""

        admin.first_name = form.first_name.data
        admin.last_name = form.last_name.data

        password = form.password.data

        if len(password) > 0:
            admin.password = hash_password(password)


        if admin.username != 'admin':
            # can not update the role for the admin account
            admin.authorization = form.authorization.data
            admin.is_active = form.is_active.data
        else:
            admin.authenticate = ADMIN_AUTH_VALUE
            admin.is_active = True

        
        if admin.email != form.email.data:
            admin.email = form.email.data

            count = Admin.query.filter(Admin.email==admin.email , Admin.username!=admin.username).count()
            if count > 0:
                form.email.errors.append('Email taken.  Please pick another')
                return admin

        try:
            db.session.commit()
        except IntegrityError:
            form.email.errors.append('Email taken.  Please pick another')

        return admin
    
    @staticmethod
    def delete(username):
        """Delete Useres"""
        admin = Admin.query.get(username)

        if admin is None:
            return {}

        admin.is_active = False

        db.session.commit()

        return {}

    @staticmethod
    def reset_password_email(form):
        """For reset password, if found the account return true"""
        
        email = form.email.data

        account = Admin.query.filter(Admin.email == email).first()

        if account:
            account.pwd_token = token_urlsafe()
            db.session.commit()

            if not is_testing():
                # send email if not testing
                mail.send_message(
                    subject='Book your services admin password reset' ,
                    sender='bobowu98@gmail.com',
                    recipients=[email] ,
                    body=f'{BASE_URL}{url_for("admin.admins_password_reset")}?token={account.pwd_token}'
                )

            return True
        return False

    
    @staticmethod
    def reset_password(form , token):
        """For reset password"""

        password = form.password.data

        return Admin.update_password_by_token(token=token , password=password)
    