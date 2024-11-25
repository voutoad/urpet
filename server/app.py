from functools import reduce
from flask import Flask, redirect, request, render_template
from models import VolunteerAnkete, db
from forms import CreateAnimalForm, LoginForm, VolunteerAnketeForm
from flask_login import (
    LoginManager,
    login_required,
    login_user,
    logout_user,
    current_user,
)
from models import User, Form, authenticate_user
from werkzeug.utils import secure_filename
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SECRET_KEY'] = 'super_secret_key'
login_manager = LoginManager(app)
login_manager.login_view = '/auth/log/'
login_manager.init_app(app)
db.init_app(app)


def check_admin():
    if not current_user.is_super_user:
        return redirect('/me')


def check_catch():
    if not current_user.is_catch:
        return redirect('/me')


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


@app.get('/auth/register/')
def reg():
    data = request.args.to_dict()
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    au = authenticate_user(username=user.username, password=data.get('password'))
    if au:
        login_user(au)
        return redirect('/me')
    return redirect('/')


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
        next = request.args.get('next')
        next = f"/add-to-cart/{user.id}/{next}/" if next else None
        return redirect(next or '/me')
    return render_template('login.html', errors=['Wrong password or username'])

# @app.post('/auth/id')
# def get_id_by_login_password():
#     data = request.args.to_dict()
#     user = authenticate_user(**data)
#     if user:
#         return user.id
#     return {'result': 'fail'}



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
        animals = [Form.query.get(_) for _ in current_user.cart.split(', ')][:-1]
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
    form = CreateAnimalForm()
    if form.validate_on_submit():
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
            'has_lost': True if form.is_lost.data is True else False,
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
    return render_template('index.html')


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
    animals = list(filter(lambda x: not x.is_approved and not x.has_lost, Form.query.all()))
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
