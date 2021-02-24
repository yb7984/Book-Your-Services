"""Modules file for handling request related to address"""

from models import Address, db
from flask import request , jsonify
from forms import AddressForm

class AddressHandler:
    """Handler for address"""

    @staticmethod
    def list(username):
        """Return address list"""

        return Address.query.filter(Address.username==username).order_by(Address.is_default.desc())

    @staticmethod
    def get(address_id):
        """Return Address"""
        return Address.query.get(address_id)

    @staticmethod
    def insert(username):
        """New Address"""
        form = AddressForm(obj=request.json, prefix="address")

        if form.validate():
            name = form.name.data
            address1 = form.address1.data
            address2 = form.address2.data
            city = form.city.data
            state = form.state.data
            zipcode = form.zipcode.data
            is_default = form.is_default.data
            is_active = form.is_active.data

            if is_active == False:
                is_default = False

            address = Address(
                username=username,
                name=name,
                address1=address1,
                address2=address2,
                city=city,
                state=state,
                zipcode=zipcode,
                is_default=is_default,
                is_active=is_active
            )

            db.session.add(address)

            try:
                db.session.commit()

                # update the is_default for other addresses
                if is_default == True:
                    AddressHandler.set_default(address)

            except:
                db.session.rollback()
                #return error message
                return {"error":"Error when adding an address"}

            #success, return new item
            return {"item":address.serialize()}

        #return form errors
        return {"errors": form.errors}

    @staticmethod
    def update(address_id):
        """Update Addresses"""
        address = Address.query.get(address_id)

        if address is None:
            return {"error":"Error when updating an address"}

        form = AddressForm(obj=request.json, prefix="address")

        if form.validate():
            address.name = form.name.data
            address.address1 = form.address1.data
            address.address2 = form.address2.data
            address.city = form.city.data
            address.state = form.state.data
            address.zipcode = form.zipcode.data
            address.is_default = form.is_default.data
            address.is_active = form.is_active.data

            # try:
            db.session.commit()

            if address.is_default == True:
                AddressHandler.set_default(address)
            # except:
            #     db.session.rollback()

            #     #return error message
            #     return {"error":"Error when updating an address"}

            #success, return new item
            return {"item":address.serialize()}

        #return form errors
        return {"errors": form.errors}
    
    @staticmethod
    def delete(address_id):
        """Delete Addresses"""
        address = Address.query.get(address_id)

        if address is None:
            return {}

        db.session.delete(address)
        db.session.commit()

        return {}
    
    @staticmethod
    def set_default(address):
        # update the is_default to False for other addresses
        list = Address.query.filter(Address.username == address.username).all()

        for item in list:
            if item.id != address.id:
                item.is_default = False
            else:
                item.is_default = True

        db.session.commit()