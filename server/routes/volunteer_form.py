from flask import render_template, redirect, request
from flask_login import login_required
from werkzeug.utils import secure_filename

from server.repo import VOLUNTEER
from server.config import BASE_DIR


@login_required
def vol_main():
    return render_template('vol.html')


@login_required
def found():
    return render_template('found.html')


@login_required
def pot():
    return render_template('poter.html')


@login_required
def ank_change():
    data = request.form.to_dict()
    files = request.files
    ank = VOLUNTEER.get_by_login(data['login'])
    if files:
        if 'photo' not in files:
            return redirect('/vol/')
        file = files['photo']
        if file.filename == '':
            return redirect('/vol/')
        filename = secure_filename(file.filename)
        uri = BASE_DIR / 'static' / 'images' / filename
        file.save(uri)
        ank.img = uri

    if 'name' in data.keys():
        ank.name = data['name']
    if 'email' in data.keys():
        ank.email = data['email']
    VOLUNTEER.save(ank)
    return redirect('/vol/')
