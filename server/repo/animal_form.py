import datetime
from typing import Type

from server.models.animal_form import Animal
from server.models.user import User
from server.models import db
from server.repo.repo import BaseRepo


class AnimalRepo(BaseRepo):
    def create(
        self,
        name: str,
        description: str,
        user_id: int,
        user: User,
        img: str,
        has_lost: bool,
        date: datetime.date,
        at_time: str,
        address: str,
        coords: str,
        is_approved: bool,
    ) -> Animal:
        animal = Animal()
        animal.name = name
        animal.description = description
        animal.user_id = user_id
        animal.user = user
        animal.img = img
        animal.has_lost = has_lost
        animal.date = date
        animal.at_time = at_time
        animal.address = address
        animal.coords = coords
        animal.is_approved = is_approved
        self.session.add(animal)
        self.session.commit()
        return animal

    def get_by_id(self, animal_id: int) -> Animal | None:
        return self.session.query(Animal).filter_by(id=animal_id).first()

    def get_py_approving(self, is_approved: bool) -> list[Type[Animal]]:
        return self.session.query(Animal).filter_by(is_approved=is_approved).all()

    def get_by_lost(self, has_lost: bool) -> list[Type[Animal]]:
        return self.session.query(Animal).filter_by(has_lost=has_lost).all()

ANIMAL = AnimalRepo(db.session)
