from flask import Flask
from flask_login import LoginManager

from server.models import db
from server.repo.user import USER

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SECRET_KEY'] = 'super_secret_key'
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = '/auth/login/'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return USER.get_by_id(user_id)
