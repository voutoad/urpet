import datetime

from sqlalchemy.orm import Mapped, mapped_column

from server.models.database import db


class VolunteerForm(db.Model):
    __tablename__ = 'volunteer_form'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    name: Mapped[str]
    description: Mapped[str]
    email: Mapped[str]
    date_of_birth: Mapped[datetime.date]
    img: Mapped[str]
    is_approved: Mapped[bool] = mapped_column(default=False)
    login: Mapped[str]
