from utils import db, hash_password, check_password_hash
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from utils import *


class Admin(db.Model):
    """Admin"""
    __tablename__ = 'admins'

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    authorization = db.Column(
        db.String(100), nullable=False, server_default="regular")

    created = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=sqlalchemy.func.now()
    )

    pwd_token = db.Column(db.Text, nullable=True)

    is_active = db.Column(db.Boolean, nullable=False, server_default="TRUE")

    @property
    def full_name(self):
        """Return the full name of the admin"""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        e = self
        return f"<Admin {e.first_name} {e.last_name} {e.email}>"

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register admin w/hashed password & return admin."""

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hash_password(password), email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """Validate that admin exists & password is correct.

        Return admin if valid; else return False.
        """

        u = Admin.query.filter_by(username=username).first()

        if u and u.is_active and check_password_hash(u.password, password):
            # return admin instance
            return u
        else:
            return False

    @classmethod
    def update_password(cls, username, password):
        """Update password"""

        u = Admin.query.filter(Admin.username==username).first()

        if u:
            u.password = hash_password(password)
            u.pwd_token = None
            db.session.commit()

            return u
        else:
            return False

    @classmethod
    def update_password_by_token(cls, token, password):
        """Update password by token"""

        u = Admin.query.filter(Admin.pwd_token==token).first()

        if u:
            u.password = hash_password(password)
            u.password_token = None
            db.session.commit()

            return u

        return False

class User(db.Model):
    """User"""
    __tablename__ = 'users'

    # regualar information
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(20))
    description = db.Column(db.Text)
    image = db.Column(db.Text)

    # for google calendar use
    calendar_id = db.Column(db.Text)
    calendar_email = db.Column(db.String(50))

    # analysis
    reviews = db.Column(db.Integer, server_default="0")
    rating = db.Column(db.Float, server_default="0")

    #provider or customer
    is_provider = db.Column(db.Boolean, nullable=False, server_default="FALSE")

    updated = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=sqlalchemy.func.now()
    )
    created = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=sqlalchemy.func.now()
    )

    pwd_token = db.Column(db.Text, nullable=True)

    is_active = db.Column(db.Boolean, nullable=False, server_default="TRUE")

    # Addresses
    addresses = db.relationship(
        "Address", backref="user", cascade="all, delete, delete-orphan", passive_deletes=True)

    # Services
    services = db.relationship(
        "Service", backref="user", cascade="all, delete, delete-orphan", passive_deletes=True)

    # Schedules
    schedules = db.relationship(
        "Schedule", backref="user", cascade="all, delete, delete-orphan", passive_deletes=True)

    @property
    def full_name(self):
        """Return the full name of the admin"""
        return f"{self.first_name} {self.last_name}"

    @property
    def image_url(self):
        """Return the image url"""
        if self.image is None or len(self.image) == 0:
            return DEFAULT_IMAGE_USER

        return upload_file_url(self.image, username=self.username)

    def __repr__(self):
        """Representation of this class"""
        e = self
        return f"<User {e.first_name} {e.last_name} {e.email}>"

    @classmethod
    def register(cls, username, password, email, first_name, last_name, is_provider):
        """Register user w/hashed password & return user."""

        # return instance of user w/username and hashed pwd
        return cls(
            username=username,
            password=hash_password(password),
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_provider=is_provider)

    @classmethod
    def authenticate(cls, username, password):
        """Validate that admin exists & password is correct.

        Return admin if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and u.is_active and check_password_hash(u.password, password):
            # return admin instance
            return u
        else:
            return False

    @classmethod
    def update_password(cls, username, password):
        """Update password"""

        u = User.query.filter(User.username==username).first()

        if u:
            u.password = hash_password(password)
            db.session.commit()

            return u
        else:
            return False

    @classmethod
    def update_password_by_token(cls, token, pwd):
        """Update password by token"""

        u = User.query.filter(User.pwd_token==token).first()

        if u:
            u.password = hash_password(pwd)
            u.password_token = None
            db.session.commit()

            return u

        return False

    def serialize(self):
        """Serialize a User SQLAlchemy obj to dictionary."""

        return {
            "username": self.username,
            "full_name": self.full_name,
            "first_name": self.first_name,
            "last_name":self.last_name,
            "email": self.email,
            "phone": self.phone,
            "description": self.description,
            "image": self.image,
            "image_url": self.image_url,
            "reviews": self.reviews,
            "rating": self.rating,
            "is_provider": self.is_provider,
            "updated": self.updated,
            "created": self.created,
            "is_active": self.is_active
        }


class Address(db.Model):
    """Address"""
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), db.ForeignKey(
        'users.username', ondelete="CASCADE"))
    name = db.Column(db.String(100), nullable=False)
    address1 = db.Column(db.String(100), nullable=False)
    address2 = db.Column(db.String(100))
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.String(20), nullable=False)
    is_default = db.Column(db.Boolean, nullable=False, server_default="true")
    is_active = db.Column(db.Boolean, nullable=False, server_default="true")

    @property
    def address(self):
        """Return the address"""
        return f"""{self.name}
{self.address1} {self.address2}
{self.city}, {self.state} {self.zipcode}"""

    def __repr__(self):
        """Representation of this class"""
        e = self
        return f"<Address {e.username} {e.address}>"

    def serialize(self):
        """Serialize a Address SQLAlchemy obj to dictionary."""

        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "address1": self.address1,
            "address2": self.address2,
            "city": self.city,
            "state": self.state,
            "zipcode": self.zipcode,
            "address": self.address,
            "is_default": self.is_default,
            "is_active": self.is_active
        }


class Category(db.Model):
    """Categories"""
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, server_default="true")

    categories_services = db.relationship(
        "CategoryService", backref="category", cascade="all, delete, delete-orphan", passive_deletes=True)
    services = db.relationship(
        "Service", secondary="categories_services", backref="categories")

    def __repr__(self):
        """Representation of this class"""
        e = self
        return f"<Category id={e.id} name={e.name}>"

    def serialize(self):
        """Serialize a Category SQLAlchemy obj to dictionary."""

        return {
            "id": self.id,
            "name": self.name,
            "is_active": self.is_active
        }




class Service(db.Model):
    """Services from the providers"""
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), db.ForeignKey(
        'users.username', ondelete="CASCADE"))
    name = db.Column(db.String(100), nullable=False)
    location_type = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text)
    updated = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=sqlalchemy.func.now()
    )
    created = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=sqlalchemy.func.now()
    )
    is_active = db.Column(db.Boolean, nullable=False, server_default="TRUE")

    categories_services = db.relationship(
        "CategoryService", backref="service", cascade="all, delete, delete-orphan", passive_deletes=True)


    @property
    def image_url(self):
        """Return the image url"""
        if self.image is None or len(self.image) == 0:
            return DEFAULT_IMAGE_SERVICE

        return upload_file_url(self.image, username=self.username , dirname="services")
    
    @property
    def location_type_name(self):
        """Return the location type name"""

        return Service.get_location_type_name(self.location_type)

    @classmethod
    def get_location_type_name(cls , location_type):
        """Return the location type name"""

        if location_type == 0:
            return "Online Service"
        if location_type == 1:
            return "Phone Service"

        return "Online Service"

    def set_categoiry_ids(self, ids=[]):
        """Set categories with category_id list"""

        self.categories_services.clear()
        for category_id in ids:
            self.categories_services.append(CategoryService(category_id=int(category_id) , service_id=self.id))
    
    
    def get_category_ids(self):
        """Return the list of the category_ids"""

        ids = []
        for item in self.categories_services:
            ids.append(item.category_id)

        return ids

    def __repr__(self):
        """Representation of this class"""
        e = self
        return f"<Service name={e.name} username={e.username}>"


    def serialize(self):
        """Serialize a Service SQLAlchemy obj to dictionary."""

        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "location_type": self.location_type ,
            "location_type_name": self.location_type_name,
            "description": self.description ,
            "image": self.image,
            "image_url": self.image_url,
            "updated": self.updated,
            "created": self.created,
            "is_active": self.is_active,
            "categories": [category.serialize()  for category in self.categories],
            "category_ids": self.get_category_ids(),
            "provider": self.user.full_name
        }

class CategoryService(db.Model):
    """Categories to Services"""
    __tablename__ = 'categories_services'

    category_id = db.Column(db.Integer, db.ForeignKey(
        "categories.id", ondelete="CASCADE"), primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey(
        "services.id", ondelete="CASCADE"), primary_key=True)

    def __repr__(self):
        """Representation of this class"""
        e = self
        return f"<CategoryService category_id={e.category_id} service_id={e.service_id}>"


class Schedule(db.Model):
    """Schedule setting for providers"""
    __tablename__ = 'schedules'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), db.ForeignKey(
        'users.username', ondelete="CASCADE"))
    schedule_type = db.Column(db.Integer, nullable=False, server_default="0")
    schedule_date = db.Column(db.Date)
    schedules = db.Column(db.Text, nullable=False, server_default="")
    is_active = db.Column(db.Boolean, nullable=False, server_default="TRUE")

    @property
    def schedule_type_name(self):
        """Return the schedule type display name"""

        if self.schedule_type == 1:
            return "Date"

        return "Weekly"

    def __repr__(self):
        """Representation of this class"""
        e = self
        return f"<Service date_exp={e.date_exp} username={e.username} start={e.start} last={e.last}>"


class Appointment(db.Model):
    """Appointments"""
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # available after generated google calendar event
    event_id = db.Column(db.Text, server_default="")
    provider_username = db.Column(db.String(20), db.ForeignKey(
        'users.username', ondelete="CASCADE"))
    customer_username = db.Column(db.String(20), db.ForeignKey(
        'users.username', ondelete="CASCADE"))
    start = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    end = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey(
        'services.id', ondelete="CASCADE"))
    location_type = db.Column(db.Integer, nullable=False, server_default="0")
    address = db.Column(db.Text, nullable=False, server_default="")
    note = db.Column(db.Text, nullable=False, server_default="")
    summary = db.Column(db.Text, nullable=False, server_default="")
    description = db.Column(db.Text, nullable=False, server_default="")
    updated = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=sqlalchemy.func.now()
    )
    created = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=sqlalchemy.func.now()
    )
    is_active = db.Column(db.Boolean, nullable=False, server_default="TRUE")

    provider = db.relationship("User", foreign_keys=[provider_username], backref=db.backref(
        "appointments_as_provider", lazy="dynamic"))

    customer = db.relationship("User", foreign_keys=[customer_username], backref=db.backref(
        "appointments_as_customer", lazy="dynamic"))

    def __repr__(self):
        """Representation of this class"""
        e = self
        return f"<Service id={e.id} provider_username={e.provider_username} customer_username={e.customer_username} start={e.start} end={e.end}>"


class Email(db.Model):
    """Emails"""
    __tablename__ = 'emails'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey(
        'appointments.id', ondelete="CASCADE"))
    sender_username = db.Column(db.String(20), db.ForeignKey(
        'users.username', ondelete="CASCADE"))
    receiver_username = db.Column(db.String(20), db.ForeignKey(
        'users.username', ondelete="CASCADE"))
    email = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_sent = db.Column(db.Boolean, nullable=False, server_default="FALSE")
    sent = db.Column(db.TIMESTAMP(timezone=True))
    created = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=sqlalchemy.func.now()
    )
    is_active = db.Column(db.Boolean, nullable=False, server_default="TRUE")

    sender = db.relationship("User", foreign_keys=[
                             sender_username], backref=db.backref("emails_sent", lazy="dynamic"))

    receiver = db.relationship("User", foreign_keys=[
                               receiver_username], backref=db.backref("emails_received", lazy="dynamic"))

    def __repr__(self):
        """Representation of this class"""
        e = self
        return f"<Email title={e.title} from={e.sender_username} to={e.receiver_username} email={e.email}>"


class Review(db.Model):
    """Reviews"""
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey(
        'appointments.id', ondelete="CASCADE"))
    from_username = db.Column(db.String(20), db.ForeignKey(
        'users.username', ondelete="CASCADE"))
    to_username = db.Column(db.String(20), db.ForeignKey(
        'users.username', ondelete="CASCADE"))
    rating = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_visible = db.Column(db.Boolean, nullable=False, server_default="FALSE")
    updated = db.Column(db.TIMESTAMP(timezone=True))
    created = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=sqlalchemy.func.now()
    )
    is_active = db.Column(db.Boolean, nullable=False, server_default="TRUE")

    from_user = db.relationship("User", foreign_keys=[
                                from_username], backref=db.backref("reviews_sent", lazy='dynamic'))

    to_user = db.relationship("User", foreign_keys=[
                              to_username], backref=db.backref("reviews_received", lazy='dynamic'))

    def __repr__(self):
        """Representation of this class"""
        e = self
        return f"<Review title={e.title} from_username={e.from_username} to_username={e.to_username} rating={e.rating}>"
