from flask import render_template, redirect, request
from flask_login import current_user, login_required

from repo import USER
from repo.animal_form import ANIMAL
from forms import CreateAnimalForm


@login_required
def me():
    try:
        animals = [ANIMAL.get_by_id(_) for _ in current_user.cart.split(', ')][
            :-1
        ]
    except Exception:
        animals = []
    return render_template('mainaccount.html', animals=animals)


@login_required
def addopt():
    animals = ANIMAL.get_py_approving(True)
    try:
        cart = list(map(int, current_user.cart.split(', ')[:-1]))
    except Exception:
        cart = []
    res = []
    sp = []
    for k, v in enumerate(animals):
        if k % 3 or k == 0:
            sp.append(v)
        else:
            res.append(sp)
            sp = [v]
    else:
        res.append(sp)
    return render_template('addopt.html', animals=res, cart=cart)


@login_required
def overexposure():
    animals = ANIMAL.get_overexposure()
    form = CreateAnimalForm()
    return render_template('overexposure.html', animals=animals, form=form)


@login_required
def urpet():
    return render_template('urpet.html')


@login_required
def poterashki():
    form = CreateAnimalForm()
    return render_template('poterashkiafter.html', form=form)


@login_required
def naydenushi():
    form = CreateAnimalForm()
    return render_template('naydenushi.html', form=form)


def add_animal(us_id, an_id):
    user = USER.get_by_id(us_id)
    if not user.cart:
        user.cart = f'{an_id}, '
    else:
        user.cart += f'{an_id}, '
    USER.save(user)
    if current_user:
        return redirect('/me')
    return {'result': 'success'}


def delete_animal(us_id, an_id):
    user = USER.get_by_id(us_id)
    if str(an_id) in user.cart.split(', '):
        user.cart = user.cart.split(', ').remove(str(an_id))
        USER.save(user)
        return {'result': 'success'}
    return {'result': 'fail'}


def update():
    data = request.form.to_dict()
    if not current_user.check_password(data['password']):
        return redirect('/me')
    if data['name']:
        current_user.name = data['name']
    if data['email']:
        current_user.email = data['email']
    USER.save(current_user)
    return redirect('/me')
