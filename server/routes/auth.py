import datetime

from flask import request, redirect, render_template
from flask_login import login_user, logout_user, login_required

from server.models.user import authenticate
from server.repo.user import USER
from server.repo.volunteer_form import VOLUNTEER


def login():
    data = request.form.to_dict()
    nexts = data['next']
    del data['next']
    user = authenticate(**data)
    if user:
        login_user(user)
        if user.is_super_user:
            return redirect('/admin/foundanimals')
        if user.is_catch:
            return redirect('/catch/lost')
        if user.is_vol:
            return redirect('/vol/')
        nexts = f'/add-to-cart/{user.id}/{nexts}/' if nexts else None
        return redirect(nexts or '/me')

    return render_template('login.html', errors=['Wrong password or username'])


def register():
    data = request.form.to_dict()
    if 'is_vol' in data.keys():
        data['is_vol'] = True
    else:
        data['is_vol'] = False

    # data['is_vol'] = data['is_vol'] == 'on'
    u = USER.create(**data)
    user = authenticate(username=u.username, password=data['password'])
    if user:
        login_user(user)
        if user.is_vol:
            VOLUNTEER.create(u.name, '', u.email, datetime.date.today(), '', u.username)
            return redirect('/vol/')
        return redirect('/me')
    return redirect('/')


@login_required
def logout():
    logout_user()
    return redirect('/')
