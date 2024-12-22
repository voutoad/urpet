from werkzeug.security import generate_password_hash

from server.models.user import User
from server.models import db
from server.repo.repo import BaseRepo


class UserRepo(BaseRepo):
    def create(
        self,
        name: str,
        username: str,
        email: str,
        password: str,
        is_super_user=False,
        is_catch=False,
        is_vol=False,
    ) -> User:
        user = User()
        user.name = name
        user.username = username
        user.email = email
        user.is_super_user = is_super_user
        user.is_vol = is_vol
        user.is_catch = is_catch
        user.password = generate_password_hash(password)
        self.session.add(user)
        self.session.commit()
        return user

    def get_by_id(self, user_id: int) -> User | None:
        return self.session.query(User).filter_by(id=user_id).first()

    def authenticate_user(
        self, username: str, password: str
    ) -> User | None | bool:
        user = self.session.query(User).filter_by(username=username).first()
        if user and user.check_password(password):
            user.is_authenticated = True
            self.session.add(user)
            self.session.commit()
            return user
        return False


USER = UserRepo(db.session)
