from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, HiddenField, BooleanField, TimeField, DateField, FileField
from wtforms.validators import DataRequired


class CreateAnimalForm(FlaskForm):
    name = StringField('Кличка', validators=[DataRequired()])
    description = StringField('Опишите', validators=[DataRequired()])
    owner = HiddenField('owner')
    is_lost = BooleanField('is_lost')
    img = FileField('Изображение', validators=[FileRequired()])
    date = DateField('Какого числа', validators=[DataRequired()])
    redirect = HiddenField('redirect')
    at_time = TimeField('Во время', validators=[DataRequired()])
    address = StringField('Где', validators=[DataRequired()])