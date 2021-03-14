"""Modules file for handling request related to category"""

from models import Category , db
from flask import request
from forms import CategoryForm
from utils import *


class CategoryHandler:
    """Handler for category"""

    @staticmethod
    def list(only_active=False):
        """Return category list"""
        
        items = None
        if only_active == False:
            items = Category.query.order_by(Category.name).order_by(Category.is_active.desc()).all()
        else:
            items = Category.query.filter(Category.is_active==True).order_by(Category.name).all()

        return items


    def list_for_select():
        """Return a category list for select field"""

        return [(str(category.id) , category.name) for category in Category.query.filter(Category.is_active==True).all()]

    @staticmethod
    def get(category_id):
        """Return Category"""
        return Category.query.get(category_id)

    @staticmethod
    def insert():
        """New Category"""
        form = CategoryForm(obj=request.json)

        if form.validate():
            name = form.name.data
            is_active = form.is_active.data

            category = Category(
                name=name,
                is_active=is_active
            )

            db.session.add(category)

            try:
                db.session.commit()

            except:
                db.session.rollback()
                # return error message
                return {"error": "Error when adding an category"}

            # success, return new item
            return {"item": category.serialize()}

        # return form errors
        return {"errors": form.errors}

    @staticmethod
    def update(category_id):
        """Update Categoryes"""
        category = Category.query.get(category_id)

        if category is None:
            # return error message
            return {"error": "Error when updating an category"}

        form = CategoryForm(obj=request.json)

        if form.validate():
            category.name = form.name.data
            category.is_active = form.is_active.data

            db.session.commit()
            
            # success, return new item
            return {"item": category.serialize()}

        # return form errors
        return {"errors": form.errors}

    @staticmethod
    def delete(category_id):
        """Delete Categoryes, Just set is_active to false"""
        category = Category.query.get(category_id)

        if category is None:
            return {}

        category.is_active = False

        db.session.commit()

        return {}
