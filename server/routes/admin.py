import smtplib
from email.mime.text import MIMEText

from flask import render_template, request
from server.forms import CreateAnimalForm
from server.repo import ANIMAL, VOLUNTEER
from server.config import SMTP_PASSWORD, SMTP_URL


def check_admin():
    ...


def add():
    check_admin()
    form = CreateAnimalForm()
    animals = ANIMAL.get_all()
    return render_template('index.html', form=form, animals=animals)


def change(form_id: int):
    form = ANIMAL.get_by_id(form_id)
    form.is_approved = True
    ANIMAL.save(form)
    return {'answer': 'checked'}


def delete(form_id: int):
    form = ANIMAL.get_by_id(form_id)
    ANIMAL.delete(form)
    return {'answer': 'checked'}


def lost_animals():
    check_admin()
    animals = ANIMAL.not_approved_has_lost()
    return render_template('lost_animals.html', pets=animals)


def found_animals():
    check_admin()
    animals = ANIMAL.not_approved_found()
    print(animals)
    return render_template('found_animals.html', animals=animals)


def vol_requests():
    check_admin()
    requests = VOLUNTEER.not_approved()
    return render_template('volunteer_requests.html', requests=requests)


def send_email():
    email = request.args.get('email')
    server = smtplib.SMTP_SSL(SMTP_URL)
    server.login('urp3t', SMTP_PASSWORD)
    msg = MIMEText('Ваша заявка одобрена!', 'plain', 'utf-8')
    msg['subject'] = email
    msg['from'] = 'urp3t@yandex.ru'
    msg['to'] = email
    server.send_message(msg)
    server.quit()
    v = VOLUNTEER.get_by_email(email)
    v.is_approved = True
    VOLUNTEER.save(v)
    return {'result': 'success'}

def delete_vol(vol_id: int):
    vol = VOLUNTEER.get_by_id(vol_id)
    VOLUNTEER.delete(vol)
    return {'result': 'success'}