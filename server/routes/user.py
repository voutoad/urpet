from flask import render_template
from flask_login import current_user, login_required

from server.repo.animal_form import ANIMAL

@login_required
def me():
    try:
        animals = [ANIMAL.get_by_id(_) for _ in current_user.cart.split(', ')][
                  :-1
                  ]
    except Exception:
        animals = []
    return render_template('mainaccount.html', animals=animals)
