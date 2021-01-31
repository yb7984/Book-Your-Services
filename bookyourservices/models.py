from utils import db, hash_password , check_password_hash
from flask_sqlalchemy import SQLAlchemy,sqlalchemy
from utils import *

class Admin(db.Model):
    """Admin"""
    __tablename__ = 'admins'

    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text , nullable=False)
    first_name = db.Column(db.String(30) , nullable=False)
    last_name = db.Column(db.String(30) , nullable=False)
    email = db.Column(db.String(30) , nullable=False)
    authorization = db.Column(db.String(100) , nullable=False , server_default="regular")
    
    created = db.Column(
        db.TIMESTAMP(timezone=True),
        nullable=False, 
        server_default=sqlalchemy.func.now()
        )

    pwd_token = db.Column(db.Text , nullable=True)

    is_active = db.Column(db.Boolean , nullable=False , server_default="TRUE")


    @property
    def full_name(self):
        """Return the full name of the admin"""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        e = self
        return f"<Admin {e.first_name} {e.last_name} {e.email}>"

    @classmethod
    def register(cls, username, password , email , first_name , last_name):
        """Register admin w/hashed password & return admin."""

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hash_password(password) , email=email , first_name= first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """Validate that admin exists & password is correct.

        Return admin if valid; else return False.
        """

        u = Admin.query.filter_by(username=username).first()

        if u and check_password_hash(u.password, password):
            # return admin instance
            return u
        else:
            return False

    @classmethod
    def update_password_by_token(cls , token , pwd):
        """Update password by token"""

        u = Admin.query.filter_by(pwd_token=token).first()

        if u:
            u.password = bcrypt.generate_password_hash(pwd)
            u.password_token = None
            db.session.commit()

            return u

        return False


class User(db.Model):
    """User"""
    __tablename__ = 'users'

    #regualar information
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text , nullable=False)
    first_name = db.Column(db.String(30) , nullable=False)
    last_name = db.Column(db.String(30) , nullable=False)
    email = db.Column(db.String(30) , nullable=False)
    phone = db.Column(db.String(20))
    description =  db.Column(db.Text)
    image = db.Column(db.Text)

    #for google calendar use
    calendar_id = db.Column(db.Text)
    calendar_email = db.Column(db.String(50))

    #analysis
    reviews = db.Column(db.Integer , server_default="0")
    rating = db.Column(db.Float , server_default="0")

    #provider or customer
    is_provider = db.Column(db.Boolean , nullable=False, server_default="FALSE")

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

    pwd_token = db.Column(db.Text , nullable=True)

    is_active = db.Column(db.Boolean , nullable=False , server_default="TRUE")

    #Addresses
    addresses = db.relationship("Address" , backref="user" , cascade="all, delete" , passive_deletes=True)

    #Services
    services = db.relationship("Service" , backref="user" , cascade="all, delete" , passive_deletes=True)


    @property
    def full_name(self):
        """Return the full name of the admin"""
        return f"{self.first_name} {self.last_name}"

    @property
    def image_url(self):
        """Return the image url"""
        return upload_file_url(self.image , USER_UPLOAD_DIRNAME)

    def __repr__(self):
        e = self
        return f"<User {e.first_name} {e.last_name} {e.email}>"

    @classmethod
    def register(cls, username, password , email , first_name , last_name , is_provider):
        """Register user w/hashed password & return user."""

        # return instance of user w/username and hashed pwd
        return cls(
            username=username, 
            password=hash_password(password) , 
            email=email , 
            first_name= first_name, 
            last_name=last_name ,
            is_provider=is_provider)

    @classmethod
    def authenticate(cls, username, password):
        """Validate that admin exists & password is correct.

        Return admin if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and check_password_hash(u.password, password):
            # return admin instance
            return u
        else:
            return False

    @classmethod
    def update_password_by_token(cls , token , pwd):
        """Update password by token"""

        u = User.query.filter_by(pwd_token=token).first()

        if u:
            u.password = bcrypt.generate_password_hash(pwd)
            u.password_token = None
            db.session.commit()

            return u

        return False

class Address(db.Model):
    """Address"""
    __tablename__ = 'addresses'

    id = db.Column(db.Integer , primary_key=True , autoincrement=True)
    username = db.Column(db.String(20), db.ForeignKey('users.username', ondelete="CASCADE"))
    name = db.Column(db.String(100) , nullable=False)
    address1 = db.Column(db.String(100) , nullable=False)
    address2 = db.Column(db.String(100))
    city = db.Column(db.String(50) , nullable=False)
    state = db.Column(db.String(50) , nullable=False)
    zipcode = db.Column(db.String(20) , nullable=False)
    is_default = db.Column(db.Boolean , nullable=False , server_default="true")
    is_active = db.Column(db.Boolean , nullable=False , server_default="true")


class Category(db.Model):
    """Categories"""
    __tablename__ = 'categories'

    id = db.Column(db.Integer , primary_key=True , autoincrement=True)
    name = db.Column(db.String(100) , nullable=False)
    is_active = db.Column(db.Boolean , nullable=False , server_default="true")

    categories_services = db.relationship("CategoryService" , backref="category" , cascade="all, delete" , passive_deletes=True)
    services = db.relationship("Service" , secondary="categories_services" , backref="categories")


class Service(db.Model):
    """Services from the providers"""
    __tablename__ = 'services'

    id = db.Column(db.Integer , primary_key=True , autoincrement=True)
    username = db.Column(db.String(20), db.ForeignKey('users.username', ondelete="CASCADE"))
    name = db.Column(db.String(100) , nullable=False)
    location_type = db.Column(db.Integer , nullable=False)
    description = db.Column(db.Text , nullable=False)
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
    is_active = db.Column(db.Boolean , nullable=False , server_default="TRUE")

    categories_services = db.relationship("CategoryService" , backref="service" , cascade="all, delete" , passive_deletes=True)
    

class CategoryService(db.Model):
    """Categories to Services"""
    __tablename__ = 'categories_services'

    category_id = db.Column(db.Integer , db.ForeignKey("categories.id", ondelete="CASCADE") , primary_key=True)
    service_id = db.Column(db.Integer , db.ForeignKey("services.id", ondelete="CASCADE") , primary_key=True)

