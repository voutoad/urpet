from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import (
    StringField,
    HiddenField,
    DateField,
    TimeField,
    BooleanField,
)
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])


class CreateAnimalForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    owner = HiddenField('owner')
    is_lost = BooleanField('is_lost')
    img = FileField('image', validators=[FileRequired()])
    date = DateField('date', validators=[DataRequired()])
    at_time = TimeField('at_time', validators=[DataRequired()])
