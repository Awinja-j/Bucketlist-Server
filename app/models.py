
from app import db
from passlib.apps import custom_app_context as pwd_context


class User(db.Model):
    '''this is the person model'''
    __tablename__ = "users"
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255),nullable=False, unique=True)
    password_hash = db.Column(db.String(128),nullable=False)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def __init__(self, name):
        """initialize with name."""
        self.person_name = person_name

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
    '''this is the bucket model'''
    __tablename__ = "bucketlists"
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    item = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    owner_id = db.column(db.Integer, db.ForeignKey('person_ID'))
    
    def __init__(self, name):
        """initialize with name."""
        self.item_name = item_name

    def __repr__(self):
        return "<Bucketlist: {}>".format(self.item_name)


    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Bucketlist.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    