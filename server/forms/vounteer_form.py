from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, DateField
from wtforms.validators import DataRequired


class CreateVolunteerForm(FlaskForm):
    name = StringField('Имя и Фамилия', validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired()])
    description = StringField('Опишите себя', validators=[DataRequired()])
    date_of_birth = DateField('Дата рождения', validators=[DataRequired()])
    img = FileField('Изображение', validators=[FileRequired()])
