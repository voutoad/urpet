import datetime

from sqlalchemy.orm import Mapped, mapped_column, backref
from server.models.database import db


class Animal(db.Model):
    __tablename__ = 'form'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    address: Mapped[str] = mapped_column(index=True)
    coords: Mapped[str] = mapped_column(index=True, default='')
    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column(index=True)
    img: Mapped[str]
    is_approved: Mapped[bool]
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=1)
    user = db.relationship('User', backref=backref('forms', uselist=True))
    has_lost: Mapped[bool]
    date: Mapped[datetime.date] = mapped_column(
        default=datetime.datetime.now().date
    )
    at_time: Mapped[str]
