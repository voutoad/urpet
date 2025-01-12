import datetime

from models.animal_form import Animal
from models.user import User
from models import db
from repo.repo import BaseRepo


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
        at_time: datetime.time,
        address: str,
        coords: str,
        is_approved: bool,
        overexposure: bool,
        for_time: str
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
        animal.for_time = for_time
        animal.address = address
        animal.coords = coords
        animal.is_approved = is_approved
        animal.overexposure = overexposure
        self.session.add(animal)
        self.session.commit()
        return animal

    def get_by_id(self, animal_id: int) -> Animal | None:
        return self.session.query(Animal).filter_by(id=animal_id).first()

    def get_py_approving(self, is_approved: bool) -> list[Animal]:
        return (
            self.session.query(Animal).filter_by(is_approved=is_approved).all()
        )

    def get_by_lost(self, has_lost: bool) -> list[Animal]:
        return (
            self.session.query(Animal)
            .filter_by(has_lost=has_lost, overexposure=False)
            .all()
        )

    def get_all(self):
        return self.session.query(Animal).all()

    def save(self, form: Animal) -> Animal:
        self.session.add(form)
        self.session.commit()
        return form

    def delete(self, form: Animal) -> int:
        n = form.id
        self.session.delete(form)
        self.session.commit()
        return n

    def not_approved_has_lost(self):
        return (
            self.session.query(Animal)
            .filter_by(has_lost=True, is_approved=False, overexposure=False)
            .all()
        )

    def approved_has_lost(self):
        return (
            self.session.query(Animal)
            .filter_by(has_lost=True, is_approved=True, overexposure=False)
            .all()
        )

    def approved_found(self):
        return (
            self.session.query(Animal)
            .filter_by(has_lost=False, is_approved=True, overexposure=False)
            .all()
        )

    def not_approved_found(self):
        return (
            self.session.query(Animal)
            .filter_by(has_lost=False, is_approved=False, overexposure=False)
            .all()
        )

    def get_overexposure(self):
        return (
            self.session.query(Animal)
            .filter_by(overexposure=True, is_approved=True)
            .all()
        )


ANIMAL = AnimalRepo(db.session)  # type: ignore
