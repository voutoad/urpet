from flask import render_template

from server.forms import CreateAnimalForm
from server.repo import ANIMAL

# route => /
def root():
    animals = ANIMAL.get_py_approving(True)
    return render_template('main.html', animals=animals)

# route => /map
def map():
    form = CreateAnimalForm()

# route => /about
def about():
    ...
