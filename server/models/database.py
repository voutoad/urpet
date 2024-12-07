from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    ...
    # id: Mapped[int] = mapped_column(primary_key=True, index=True)


db = SQLAlchemy(model_class=Base)
