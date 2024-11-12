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
    name = StringField('Кличка', validators=[DataRequired()])
    description = StringField('Опишите', validators=[DataRequired()])
    owner = HiddenField('owner')
    is_lost = BooleanField('is_lost')
    img = FileField('Изображение', validators=[FileRequired()])
    date = DateField('Какого числа', validators=[DataRequired()])
    redirect = HiddenField('redirect')
    at_time = TimeField('Во время', validators=[DataRequired()])
