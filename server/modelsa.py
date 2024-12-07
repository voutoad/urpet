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
    is_vol = db.Column(db.Boolean, default=False)
    chat_active = db.Column(db.Boolean, default=False)
    personal_chat = db.Column(db.Integer, default=0)
    cart = db.Column(db.String(1000), default='')

    def __init__(
        self,
        name,
        username,
        password,
        email,
        is_super_user=False,
        is_catch=False,
        is_vol=False,
    ):
        self.name = name
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.is_super_user = is_super_user
        self.is_catch = is_catch
        self.is_vol = is_vol == 'on'

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str(self.id)

    def get(id):
        return User.query.filter_by(id=id).first()


class Form(db.Model):
    __tablename__ = 'form'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), index=True)
    coords = db.Column(db.String(20), index=True, default='')
    name = db.Column(db.String(20), index=True)
    description = db.Column(db.String(300), index=True)
    img = db.Column(db.String(500))
    is_approved = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=1)
    user = db.relationship('User', backref=backref('forms', uselist=True))
    has_lost = db.Column(db.Boolean)
    date = db.Column(db.DateTime, default=datetime.datetime.now().date)
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
        address,
        coords,
        is_approved,
    ):
        self.name = name
        self.description = description
        self.user_id = user_id
        self.user = user
        self.img = img
        self.has_lost = has_lost
        self.date = date
        self.at_time = str(at_time)
        self.address = address
        self.coords = coords
        self.is_approved = is_approved


class VolunteerAnkete(db.Model):
    __tablename__ = 'volunteer_ankete'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True)
    description = db.Column(db.String(150), index=True)
    email = db.Column(db.String(254), index=True)
    date_of_birth = db.Column(db.String(254), index=True)
    img = db.Column(db.String(500))
    is_approved = db.Column(db.Boolean, default=False)
    login = db.Column(db.String(20), index=True)

    def __init__(self, name, description, email, date_of_birth, img, login):
        self.name = name
        self.description = description
        self.email = email
        self.date_of_birth = date_of_birth
        self.img = img
        self.login = login


class Room(db.Model):
    __tablename__ = 'room'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), index=True)
    users = db.Column(db.String(20), index=True)

    def __init__(self, code, users) -> None:
        self.code = code
        self.users = users


class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    message_text = db.Column(db.String(1000), index=True)
    sender = db.Column(db.Integer, index=True)
    sent_at = db.Column(db.DateTime, default=datetime.datetime.now())
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship('Room', backref=backref('messages', uselist=True))

    def __init__(self, message, sender, room, room_id) -> None:
        self.message_text = message
        self.sender = sender
        self.room = room
        self.room_id = room_id


def authenticate_user(username='', password='') -> str | bool:
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        user.is_authenticated = True
        db.session.add(user)
        db.session.commit()
        return user
    return False
