import os
import random
import smtplib
from email.mime.text import MIMEText
from string import ascii_letters

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_socketio import SocketIO
from forms import CreateAnimalForm, VolunteerAnketeForm
from models import (
    Form,
    Room,
    User,
    VolunteerAnkete,
    authenticate_user,
    db,
)
from werkzeug.utils import secure_filename
import requests

load_dotenv()

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SECRET_KEY'] = 'super_secret_key'
login_manager = LoginManager(app)
login_manager.login_view = '/auth/log/'
login_manager.init_app(app)
db.init_app(app)
socketio = SocketIO(app)
STATIC_API_KEY = '8d088d67-b862-4454-93f6-ef870753f7be'


def check_admin():
    if not current_user.is_super_user:
        return redirect('/me')


def check_catch():
    if not current_user.is_catch:
        return redirect('/me')


def get_coords_by_address(address: str) -> str:
    resp = requests.get(
        f'https://geocode-maps.yandex.ru/1.x/?apikey={STATIC_API_KEY}&geocode={address}&format=json'
    ).json()
    return resp['response']['GeoObjectCollection']['featureMember'][0][
        'GeoObject'
    ]['Point']['pos']


def generate_room_codes(length: int, existing_codes: list[str]) -> str:
    while True:
        code_chars = [random.choice(ascii_letters) for _ in range(length)]
        code = ''.join(code_chars)
        if code not in existing_codes:
            return code


@app.route('/send-email')
def send_mail():
    email = request.args.get('email')
    server = smtplib.SMTP_SSL('smtp.yandex.ru:465')
    server.login('urp3t', os.getenv('SMTP_PASSWORD'))
    msg = MIMEText('Ваша заявка одобрена!', 'plain', 'utf-8')
    msg['Subject'] = email
    msg['From'] = 'urp3t@yandex.ru'
    msg['To'] = email
    server.send_message(msg)
    server.quit()
    v = VolunteerAnkete.query.filter_by(email=email).first()
    v.is_approved = True
    db.session.add(v)
    db.session.commit()
    return {'result': 'success'}


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/new-vol/', methods=['GET', 'POST'])
def new_vol():
    return {}


@app.post('/auth/register/')
def reg():
    data = request.form.to_dict()
    u = User(**data)
    db.session.add(u)
    db.session.commit()
    au = authenticate_user(username=u.username, password=data['password'])
    if au:
        login_user(au)
        if u.is_vol:
            db.session.add(
                VolunteerAnkete(u.name, '', u.email, '', '', u.username)
            )
            db.session.commit()
            return redirect('/vol/')
        return redirect('/me')
    return redirect('/')


@app.route('/create-chat/<string:login>')
def create_room(login: str):
    codes = [_.code for _ in Room.query.all()]
    room = generate_room_codes(15, codes)
    db.session.add(Room(code=room, users=f'{login}, '))
    db.session.commit()
    return {'result': 'success'}


@app.route('/auth/log/')
def log():
    return render_template('login.html')


@app.get('/auth/login/')
def login():
    data = request.args.to_dict().copy()
    print(request.args.get('next'))
    del data['next']
    user = authenticate_user(**data)
    if user:
        login_user(user)
        if user.is_super_user:
            return redirect('/admin/foundanimals')
        if user.is_catch:
            return redirect('/catch/lost')
        if user.is_vol:
            return redirect('/vol/')
        next = request.args.get('next')
        next = f'/add-to-cart/{user.id}/{next}/' if next else None
        return redirect(next or '/me')
    return render_template('login.html', errors=['Wrong password or username'])


@app.route('/auth/logout/')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/add-to-cart/<int:us_id>/<int:an_id>/')
def add_animal(us_id, an_id):
    user = User.query.get(us_id)
    if not user.cart:
        user.cart = f'{an_id}, '
    else:
        user.cart += f'{an_id}, '
    db.session.add(user)
    db.session.commit()
    if current_user:
        return redirect('/me')
    return {'result': 'success'}


@app.route('/get-lost/', methods=['GET'])
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
        for i in Form.query.filter(Form.has_lost)
    ]


@app.route('/poter/', methods=['GET'])
def poter():
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
        for i in Form.query.filter(Form.has_lost == 0)
    ]


@app.route('/delete-from-cart/<int:us_id>/<int:an_id>/')
def delete_animal(us_id, an_id):
    user = User.query.get(us_id)
    if str(an_id) in user.cart.split(', '):
        user.cart = user.cart.split(', ').remove(str(an_id))
        db.session.add(user)
        db.session.commit()
        return {'result': 'success'}
    return {'result': 'fail'}


@app.route('/', methods=['get'])
def main():
    print(app.instance_path.strip('instance'))
    animals = list(filter(lambda x: x.is_approved is True, Form.query.all()))
    return render_template('main.html', animals=animals)


@app.route('/map')
def map_an():
    form = CreateAnimalForm()
    return render_template('poterashki.html', form=form)


@app.route('/about', methods=['GET', 'POST'])
def about():
    f = VolunteerAnketeForm()
    if f.validate_on_submit():
        p = f.img.data
        filename = secure_filename(p.filename)
        uri = os.path.join(
            app.instance_path.strip('instance') + 'static', 'images', filename
        )
        data = {
            'name': f.name.data,
            'email': f.email.data,
            'description': f.description.data,
            'date_of_birth': f.date_of_birth.data,
            'img': uri.split('server/')[-1],
        }
        v = VolunteerAnkete(**data)
        p.save(uri)
        db.session.add(v)
        db.session.commit()
        return redirect('/about')
    return render_template('about.html', form=f)


@app.route('/me')
@login_required
def me():
    try:
        animals = [Form.query.get(_) for _ in current_user.cart.split(', ')][
            :-1
        ]
    except Exception:
        animals = []
    return render_template('mainaccount.html', animals=animals)


@app.route('/addopt')
@login_required
def addopt():
    animals = list(filter(lambda x: x.is_approved is True, Form.query.all()))
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


@app.route('/overexposure')
@login_required
def overexposure():
    return render_template('overexposure.html')


@app.route('/urpet')
@login_required
def urpet():
    return render_template('urpet.html')


@app.route('/poterashki/')
@login_required
def poterashki():
    form = CreateAnimalForm()
    return render_template('poterashkiafter.html', form=form)


@app.route('/naydenushi')
@login_required
def naydenushi():
    form = CreateAnimalForm()
    return render_template('naydenushi.html', form=form)


@app.route('/create-form/', methods=['get', 'post'])
def new_animal():
    appr = False
    if current_user and current_user.is_super_user:
        appr = True
    form = CreateAnimalForm()
    print(form)
    if form.validate_on_submit():
        print('IIII')
        p = form.img.data
        filename = secure_filename(p.filename)
        uri = os.path.join(
            app.instance_path.strip('instance') + 'static', 'images', filename
        )
        data = {
            'name': form.name.data,
            'description': form.description.data,
            'user_id': form.owner.data,
            'user': User.query.filter_by(id=form.owner.data).first(),
            'img': uri.split('server/')[-1],
            'date': form.date.data,
            'at_time': form.at_time.data,
            'has_lost': form.is_lost.data,
            'address': form.address.data,
            'coords': get_coords_by_address(form.address.data),
            'is_approved': appr,
        }
        p.save(uri)
        f = Form(**data)
        db.session.add(f)
        db.session.commit()
        return redirect(form.redirect.data)
    return render_template('animals/create.html', form=form)


@app.route('/admin/add')
@login_required
def add():
    check_admin()
    form = CreateAnimalForm()
    animals = Form.query.all()
    return render_template('index.html', animals=animals, form=form)


@app.route('/admin/change-form/<int:id>/')
def change(id):
    f = Form.query.get(id)
    f.is_approved = True
    db.session.add(f)
    db.session.commit()
    return {'answer': 'checked'}


@app.route('/admin/delete-form/<int:id>/')
def delete(id):
    f = Form.query.get(id)
    db.session.delete(f)
    db.session.commit()
    return {'answer': 'checked'}


@app.route('/admin/lostanimals')
@login_required
def lost_animals():
    check_admin()
    animals = list(
        filter(lambda x: not x.is_approved and x.has_lost, Form.query.all())
    )
    return render_template('lost_animals.html', pets=animals)


@app.route('/admin/foundanimals')
@login_required
def found_animals():
    check_admin()
    animals = list(
        filter(
            lambda x: not x.is_approved and not x.has_lost, Form.query.all()
        )
    )
    return render_template('found_animals.html', animals=animals)


@app.route('/admin/volrequests')
@login_required
def vol_requests():
    check_admin()
    requests = list(
        filter(lambda x: not x.is_approved, VolunteerAnkete.query.all())
    )
    return render_template('volunteer_requests.html', requests=requests)


@app.route('/catch/lost/', methods=['GET'])
@login_required
def catch_lost():
    animals = list(
        filter(
            lambda x: x.has_lost is True and x.is_approved, Form.query.all()
        )
    )
    return render_template('catch2.html', animals=animals)


@app.route('/catch/found/')
@login_required
def catch_found():
    animals = list(
        filter(
            lambda x: x.has_lost is False and x.is_approveda, Form.query.all()
        )
    )
    return render_template('catch.html', animals=animals)


@app.route('/vol/', methods=['GET'])
@login_required
def vol_main():
    return render_template('vol.html')


@app.route('/vol/found', methods=['GET'])
@login_required
def found():
    return render_template('found.html')


@app.route('/vol/pot', methods=['GET'])
@login_required
def pot():
    return render_template('poter.html')


@app.post('/change-ankete/')
def ank_change():
    data = request.form.to_dict()
    files = request.files
    ank = VolunteerAnkete.query.filter(
        VolunteerAnkete.login == data['login']
    ).first()
    if files:
        if 'photo' not in files:
            return redirect('/vol/')
        file = files['photo']
        if file.filename == '':
            return redirect('/vol/')
        filename = secure_filename(file.filename)
        uri = os.path.join(
            app.instance_path.strip('instance') + 'static',
            'images',
            filename,
        )
        file.save(uri)
        ank.img = uri

    if 'name' in data.keys():
        ank.name = data['name']
    if 'email' in data.keys():
        ank.email = data['email']
    db.session.add(ank)
    db.session.commit()
    return redirect('/vol/')


@app.post('/update-profile/')
def update():
    data = request.form.to_dict()
    if not current_user.check_password(data['password']):
        return redirect('/me')
    if data['name']:
        current_user.name = data['name']
    if data['email']:
        current_user.email = data['email']
    db.session.add(current_user)
    db.session.commit()
    return redirect('/me')


# @socketio.on('connect')
# def handle_connect():
#     room = session.get('room')
#     if room not in [_.code for _ in Room.query.all()]:
#         return
#     join_room(room)
#     send({
#         "sender": "",
#         "message": f"{name} начал(а) с вами чат!"
#     }, to=room)
#     r = Room.query.filter(Room.code == room).first()
#     r.users += current_user.login
#     db.session.add(r)
#     db.session.commit()


# @socketio.on('message')
# def handle_message(payload):
#     room = session.get('current_room')
#     name = current_user.name
#     if room not in [_.code for _ in Room.query.all()]:
#         return
#     message = {
#         'sender': name,
#         'message': payload
#     }
#     send(message, to=room)
#     db.session.add(Message(message=payload, sender=current_user.id, room=Room.query.filter(Room.code==room).first()))
#     db.session.commit()


# @socketio.on('disconnect')
# def handle_disconnecy():
#     room = session.get('current_room')
#     login = current_user.username

#     leave_room(room)
#     if room in [_.code for _ in Room.query.all()]:
#         r = Room.query.filter(Room.code == room).first()
#         r.users = r.users.strip(login)
#         if r.users == ", ":
#             db.session.delete(r)
#         else:
#             db.session.add(r)
#         db.session.commit()
#     send(f"{current_user.name} вышел(-шла) из чата", to=room)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.get(1):
            db.session.add(User('', '', '', ''))
        if not User.query.get(2):
            db.session.add(
                User('ADMIN', 'admin', '12345678', '', is_super_user=True)
            )
        if not User.query.get(3):
            db.session.add(
                User('CATCH', 'catch', '12345678', '', is_catch=True)
            )
        db.session.commit()
    app.run(host='0.0.0.0', debug=True)
    # socketio.run(app, host='0.0.0.0', port=5000)
