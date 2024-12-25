from models.database import db
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash


class User(db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    name: Mapped[str] = mapped_column(index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(index=True)
    is_authenticated: Mapped[str] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_anonymous: Mapped[bool] = mapped_column(default=False)
    is_super_user: Mapped[bool] = mapped_column(default=False)
    is_catch: Mapped[bool] = mapped_column(default=False)
    is_vol: Mapped[bool] = mapped_column(default=False)
    # chat_active: Mapped[bool] = mapped_column(default=False)
    # personal_chat: Mapped[int]
    cart: Mapped[str] = mapped_column(default='')

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def get_id(self):
        return str(self.id)


def authenticate(username: str, password: str) -> User | bool:
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        user.is_authenticated = True
        db.session.add(user)
        db.session.commit()
        return user
    return False
