from flask import redirect, render_template
from flask_login import current_user
from repo import ANIMAL


def is_catch():
    if not current_user.is_catch:
        return redirect('/me')


def catch_lost():
    is_catch()
    animals = ANIMAL.approved_has_lost()
    return render_template('catch2.html', animals=animals)


def catch_found():
    is_catch()
    animals = ANIMAL.approved_found()
    return render_template('catch.html', animals=animals)
