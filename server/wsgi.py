import server.config
from server.routes.urls import app
from server.app import db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print(server.config.BASE_DIR)
    app.run()
