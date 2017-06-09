# This is where you define the models of your application.
# This may be split into several modules in the same way as views.py.
import os
import inspect
import sys
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from datetime import datetime
from werkzeug.security import generate_password_hash, \
     check_password_hash
from flask_login import UserMixin
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from run import app, db


class User(db.Model, UserMixin):
    """this is the person model"""
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    bucketlist = db.relationship('Bucketlist', backref='user', lazy='dynamic')

    def __init__(self, email, password):
        """initialize with name."""
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user


    def __repr__(self):
        return "<User: {}>".format(self.email)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return User.query.all()

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
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item = db.relationship('Item', backref='bucketlist', lazy='dynamic')

    def __init__(self, title, created_by):
        """initialize with name."""
        self.title = title
        self.created_by = created_by
        self.date_created = datetime.utcnow()
        self.date_modified = datetime.utcnow()

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
    """this is the bucketlist item model"""
    __tablename__ = "item"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey("bucketlist.id"))

    def __init__(self, title, bucketlist_id):
        """initialize with name."""
        self.title = title
        self.bucketlist_id = bucketlist_id
        self.date_created = datetime.utcnow()
        self.date_modified = datetime.utcnow()
        self.done = False

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

