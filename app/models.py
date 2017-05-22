
from app import db
from passlib.apps import custom_app_context as pwd_context
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView



admin = Admin()

class User(db.Model):
    '''this is the person model'''
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255),nullable=False, unique=True)
    password_hash = db.Column(db.String(128),nullable=False)
    bucketlist = db.relationship('Bucketlist', backref = 'user', lazy='dynamic')

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def __init__(self, name):
        """initialize with name."""
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __repr__(self):
        return "<Person: {}>".format(self.person_name)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Person.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

     

class Bucketlist(db.Model):
    '''this is the bucketlist model'''
    __tablename__ = "bucketlist"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    users_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    item = db.relationship('Item', backref = 'bucketlist', lazy='dynamic')

    
    def __init__(self, title):
        """initialize with name."""
        self.title = title

    def __repr__(self):
        return "<Bucketlist: {}>".format(self.title)


    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Bucketlist.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Item(db.Model):
    '''this is the bucketlist item model'''
    __tablename__ = "item"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    bucketlist_id = db.Column(db.Integer, db.ForeignKey("bucketlist.id"))

    def __init__(self, title):
        """initialize with name."""
        self.title = title

    def __repr__(self):
        return "<Item : {}>".format(self.title)


    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Item.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Bucketlist, db.session))
admin.add_view(ModelView(Item, db.session))
    