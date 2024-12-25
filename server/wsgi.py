import server.config
from server.routes.urls import app
from server.app import db
from server.models import User

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.get(1):
            u = User()
            u.name = ''
            u.email = ''
            u.password = ''
            u.username = ''
            db.session.add(u)
        if not User.query.get(2):
            u = User()
            u.name = 'ADMIN'
            u.email = ''
            u.password = '12345678'
            u.username = 'admin'
            u.is_super_user = True
            db.session.add(u)
        if not User.query.get(3):
            u = User()
            u.name = 'CATCH'
            u.email = ''
            u.password = '12345678'
            u.username = 'catch'
            u.is_catch = True
            db.session.add(u)
        db.session.commit()
    print(server.config.BASE_DIR)
    app.run()
