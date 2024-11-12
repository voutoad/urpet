import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True)
    username = db.Column(db.String(20), index=True)
    password = db.Column(db.String(20), index=True)
    email = db.Column(db.String(254), index=True)
    is_authenticated = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    is_anonymous = db.Column(db.Boolean, default=False)
    is_super_user = db.Column(db.Boolean, default=False)
    is_catch = db.Column(db.Boolean, default=False)
    cart = db.Column(db.String(1000), default='')

    def __init__(self, name, username, password, email, is_super_user=False, is_catch=False):
        self.name = name
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.is_super_user = is_super_user
        self.is_catch = is_catch

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str(self.id)

    def get(id):
        return User.query.filter_by(id=id).first()


class Form(db.Model):
    __tablename__ = 'form'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True)
    description = db.Column(db.String(300), index=True)
    img = db.Column(db.String(500))
    is_approved = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=1)
    user = db.relationship('User', backref=backref('forms', uselist=True))
    has_lost = db.Column(db.Boolean)
    date = db.Column(db.DateTime, default=datetime.datetime.now())
    at_time = db.Column(db.String(8), default='')

    def __init__(
        self,
        name,
        description,
        user_id,
        user,
        img,
        has_lost,
        date: datetime.datetime,
        at_time,
    ):
        self.name = name
        self.description = description
        self.user_id = user_id
        self.user = user
        self.img = img
        self.has_lost = has_lost
        self.date = date
        self.at_time = str(at_time)


class VolunteerAnkete(db.Model):
    __tablename__ = 'volunteer_ankete'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True)
    description = db.Column(db.String(150), index=True)
    email = db.Column(db.String(254), index=True)
    date_of_birth = db.Column(db.String(254), index=True)
    img = db.Column(db.String(500))
    
    def __init__(self, name, description, email, date_of_birth, img):
        self.name = name
        self.description = description
        self.email = email
        self.date_of_birth = date_of_birth
        self.img = img


def authenticate_user(username='', password='') -> str | bool:
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        user.is_authenticated = True
        db.session.add(user)
        db.session.commit()
        return user
    return False
