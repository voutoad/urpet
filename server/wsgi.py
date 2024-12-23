import server.config
from server.routes.urls import app
from server.app import db
from server.models import User

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
    print(server.config.BASE_DIR)
    app.run()
