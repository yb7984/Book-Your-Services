"""Modules file for handling request related to service"""

from models import Service, CategoryService , Category , db
from flask import request, jsonify
from forms import ServiceForm
from utils import *
from views.modules.category import CategoryHandler
import datetime


class ServiceHandler:
    """Handler for service"""

    @staticmethod
    def list(username):
        """Return service list"""

        return Service.query.filter(
            Service.username == username).order_by(Service.updated.desc())

    @staticmethod
    def servicees_get(service_id):
        """Return Service"""
        return Service.query.get(service_id)

    @staticmethod
    def insert(username):
        """New Service"""
        form = ServiceForm(obj=request.json, prefix="service")
        form.categories.choices = CategoryHandler.list_for_select()

        if form.validate():
            name = form.name.data
            location_type = form.location_type.data
            description = form.description.data
            is_active = form.is_active.data

            categories = form.categories.data

            service = Service(
                username=username,
                name=name,
                description=description,
                location_type=location_type,
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


            #append the categories
            if len(categories) > 0:
                service.set_categoiry_ids(categories)

                try:
                    db.session.commit()
                except:
                    db.session.rollback()

            ServiceHandler.upload(service , form)

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
        form.categories.choices = CategoryHandler.list_for_select()
        
        if form.validate():
            service.name = form.name.data
            service.location_type = form.location_type.data
            service.description = form.description.data
            service.is_active = form.is_active.data
            service.updated = datetime.datetime.now()

            categories = form.categories.data

            service.set_categoiry_ids(categories)

            db.session.commit()
            
            #upload the image
            ServiceHandler.upload(service , form)

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

        db.session.delete(service)
        db.session.commit()

        return {}

    @staticmethod
    def upload(service , form):
        """Upload image"""

        old_file = service.image
        try:
            #upload file
            image = upload_file(
                form.image.name,
                name=service.id,
                dirname=upload_dir_user(service.username , "services"),
                exts=IMAGE_ALLOWED_EXTENSIONS)

            if image is not None:
                service.image = image
                # update the image information
                db.session.commit()
        except:
            service.image = old_file

            db.session.rollback()

