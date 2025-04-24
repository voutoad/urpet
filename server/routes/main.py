import os

from flask import render_template, redirect
from werkzeug.utils import secure_filename

from forms import CreateAnimalForm, CreateVolunteerForm
from repo import ANIMAL, VOLUNTEER
from models import VolunteerForm
from config import BASE_DIR


# route -> /
def root():
    animals = ANIMAL.get_py_approving(True)
    return render_template('main.html', animals=animals)


# route -> /map
def map_animals():
    form = CreateAnimalForm()
    return render_template('poterashki.html', form=form)


# route -> /about
def about():
    f = CreateVolunteerForm()
    if f.validate_on_submit():
        p = f.img.data
        filename = secure_filename(p.filename)
        uri = BASE_DIR / 'static' / 'images' / filename
        data = {
            'name': f.name.data,
            'email': f.email.data,
            'description': f.description.data,
            'date_of_birth': f.date_of_birth.data,
            'img': str(uri).split('server/')[-1],
            'login': f.email.data,
        }
        v = VolunteerForm(**data)
        p.save(uri)
        VOLUNTEER.save(v)
        return redirect('/about')
    return render_template('about.html', form=f)


# route -> /creators
def creators():
    form = CreateAnimalForm()
    return render_template('creators.html', form=form)
