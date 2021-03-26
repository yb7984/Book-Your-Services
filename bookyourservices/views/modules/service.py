"""Modules file for handling request related to service"""

from models import Service, CategoryService, Category, db
from flask import request, jsonify
from forms import ServiceForm
from utils import *
from views.modules.category import CategoryHandler
import datetime


class ServiceHandler:
    """Handler for service"""

    @staticmethod
    def list_by_username(username):
        """Return service list"""

        return Service.query.filter(
            Service.username == username).order_by(Service.is_active.desc(), Service.updated.desc())

    @staticmethod
    def list(username='', only_active=True, per_page=12):
        """Return service list"""

        page = int(request.args.get("page", 1))

        if username.lower().strip() == '':
            username = request.args.get('username' , '').lower().strip()
        term = request.args.get('term', '')
        categories = request.args.get('categories', '')
        is_active = request.args.get('is_active', '')

        if only_active == True:
            is_active = "1"

        
        limit = int(request.args.get("limit" , -1))
        if limit > 0:
            per_page = limit
        else:
            per_page = int(request.args.get("per_page" , per_page))

        filters = []

        if len(username) > 0:
            filters.append(Service.username==username)

        if len(term) > 0:
            filters.append(
                Service.name.like(f'%{term}%') |
                Service.description.like(f'%{term}%')
            )

        if len(categories) > 0:
            category_ids = [int(category) for category in categories.split(',') if int(category) > 0]
        
            if len(category_ids) > 0:
                filters.append(Service.id.in_(db.session.query(CategoryService.service_id).filter(
                    CategoryService.category_id.in_(category_ids))))

        if len(is_active) > 0:
            filters.append(Service.is_active == (
                True if is_active == '1' else False))

        return Service.query.filter(*tuple(filters)).order_by(Service.is_active.desc(), Service.updated.desc()).paginate(page, per_page=per_page)

    @staticmethod
    def get(service_id):
        """Return Service"""
        return Service.query.get(service_id)

    @staticmethod
    def insert(username):
        """New Service"""
        form = ServiceForm(obj=request.json, prefix="service")
        form.category_ids.choices = CategoryHandler.list_for_select()

        if form.validate():
            name = form.name.data
            description = form.description.data
            is_active = form.is_active.data

            category_ids = form.category_ids.data

            service = Service(
                username=username,
                name=name,
                description=description,
                is_active=is_active,
                updated=datetime.datetime.now(),
                created=datetime.datetime.now()
            )

            db.session.add(service)

            try:
                db.session.commit()

            except:
                db.session.rollback()
                # return error message
                return {"error": "Error when adding an service"}

            # append the categories
            if len(category_ids) > 0:
                service.set_categoiry_ids(category_ids)

                try:
                    db.session.commit()
                except:
                    db.session.rollback()

            ServiceHandler.upload(service, form)

            # success, return new item
            return {"item": service.serialize()}

        # return form errors
        return {"errors": form.errors}

    @staticmethod
    def update(service_id):
        """Update Servicees"""
        service = Service.query.get(service_id)

        if service is None:
            # return error message
            return {"error": "Error when updating an service"}

        form = ServiceForm(obj=request.json, prefix="service")
        form.category_ids.choices = CategoryHandler.list_for_select()

        if form.validate():
            service.name = form.name.data
            service.description = form.description.data
            service.is_active = form.is_active.data
            service.updated = datetime.datetime.now()

            category_ids = form.category_ids.data

            service.set_categoiry_ids(category_ids)

            db.session.commit()

            # upload the image
            ServiceHandler.upload(service, form)

            # success, return new item
            return {"item": service.serialize()}

        # return form errors
        return {"errors": form.errors}

    @staticmethod
    def delete(service_id):
        """Delete Servicees"""
        service = Service.query.get(service_id)

        if service is None:
            return {}

        service.is_active = False
        # db.session.delete(service)
        db.session.commit()

        return {}

    @staticmethod
    def upload(service, form):
        """Upload image"""

        old_file = service.image
        try:
            # upload file
            image = upload_file(
                form.image.name,
                name=service.id,
                dirname=SERVICE_UPLOAD_DIRNAME,
                exts=IMAGE_ALLOWED_EXTENSIONS)

            if image is not None:
                service.image = image
                # update the image information
                db.session.commit()
        except:
            service.image = old_file

            db.session.rollback()
