import requests
from flask import redirect, render_template
from flask_login import current_user
from werkzeug.utils import secure_filename

from forms import CreateAnimalForm
from models import User
from repo import ANIMAL, USER
from config import GEOCODE, BASE_DIR


def get_coords_by_address(address: str) -> str:
    resp = requests.get(
        f'https://geocode-maps.yandex.ru/1.x/?apikey={GEOCODE}&geocode={address}&format=json'
    ).json()
    print(resp)
    return resp['response']['GeoObjectCollection']['featureMember'][0][
        'GeoObject'
    ]['Point']['pos']


def new_animal():
    appr = False
    if (
            current_user
            and isinstance(current_user, User)
            and current_user.is_authenticated
            and current_user.is_super_user
    ):
        appr = True
    form = CreateAnimalForm()
    if form.validate_on_submit():
        print(form.at_time.data)
        p = form.img.data
        filename = secure_filename(p.filename)
        uri = BASE_DIR / 'static' / 'images' / filename
        data = {
            'name': form.name.data,
            'description': form.description.data,
            'user_id': form.owner.data,
            'user': USER.get_by_id(form.owner.data),
            'img': str(uri).split('server/')[-1],
            'date': form.date.data,
            'at_time': form.at_time.data,
            'has_lost': form.is_lost.data,
            'address': form.address.data,
            'coords': get_coords_by_address(form.address.data), # 
            'is_approved': appr,
            'overexposure': form.overexposure.data,
            'for_time': form.for_time.data,
        }
        p.save(uri)
        ANIMAL.create(**data)
        return redirect(form.redirect.data)
    print(form)
    return render_template('animals/create.html', form=form)


def get_lost():
    return [
        {
            'id': i.id,
            'name': i.name,
            'address': i.address,
            'time': f'В {i.at_time}, {i.date}',
            'description': i.description,
            'coords': list(map(float, i.coords.split())),
            'photo': i.img,
        }
        for i in ANIMAL.get_by_lost(True)
    ]


def found_animal():
    return [
        {
            'id': i.id,
            'name': i.name,
            'address': i.address,
            'time': f'В {i.at_time}, {i.date}',
            'description': i.description,
            'coords': list(map(float, i.coords.split())),
            'photo': i.img,
        }
        for i in ANIMAL.get_by_lost(False)
    ]
